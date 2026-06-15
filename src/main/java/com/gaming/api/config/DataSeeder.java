package com.gaming.api.config;

import com.gaming.api.entity.Match;
import com.gaming.api.entity.MatchPlayer;
import com.gaming.api.entity.Player;
import com.gaming.api.repository.MatchPlayerRepository;
import com.gaming.api.repository.MatchRepository;
import com.gaming.api.repository.PlayerRepository;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;

@Component
@RequiredArgsConstructor
public class DataSeeder implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataSeeder.class);

    private final PlayerRepository playerRepository;
    private final MatchRepository matchRepository;
    private final MatchPlayerRepository matchPlayerRepository;
    private final JdbcTemplate jdbcTemplate;

    @Value("${app.seed.enabled:true}")
    private boolean seedEnabled;

    @Value("${app.seed.players:10000}")
    private int playerCount;

    @Value("${app.seed.matches:200000}")
    private int matchCount;

    private static final String[] REGIONS = {"EU", "NA", "ASIA", "SA"};
    private static final String[] GAME_MODES = {"RANKED", "CASUAL", "TOURNAMENT"};
    private static final String[] STATUSES = {"FINISHED", "FINISHED", "FINISHED", "IN_PROGRESS", "PENDING"};
    private static final String[] RESULTS = {"WIN", "LOSS", "DRAW"};

    @Override
    public void run(String... args) throws Exception {
        if (!seedEnabled) return;

        long existingPlayers = playerRepository.count();
        if (existingPlayers >= playerCount) {
            log.info("Data already seeded ({} players). Skipping.", existingPlayers);
            return;
        }

        log.info("Starting data seed: {} players, {} matches...", playerCount, matchCount);
        long start = System.currentTimeMillis();

        seedPlayers();
        seedMatchesBatch();

        long elapsed = System.currentTimeMillis() - start;
        log.info("Seed complete in {}ms. Players: {}, Matches: {}",
                elapsed, playerRepository.count(), matchRepository.count());
    }

    private void seedPlayers() {
        log.info("Seeding {} players via JDBC batch...", playerCount);
        Random rng = new Random(42);

        // Batch insert via JDBC pour performance du seed
        List<Object[]> batch = new ArrayList<>(1000);
        for (int i = 1; i <= playerCount; i++) {
            String region = REGIONS[rng.nextInt(REGIONS.length)];
            int mmr = 500 + rng.nextInt(2500);
            LocalDateTime created = LocalDateTime.now().minusDays(rng.nextInt(365));
            batch.add(new Object[]{
                "player_" + i,
                "player" + i + "@gaming.com",
                mmr,
                region,
                created
            });
            if (batch.size() == 1000) {
                jdbcTemplate.batchUpdate(
                    "INSERT INTO players (username, email, mmr, region, created_at) VALUES (?,?,?,?,?)",
                    batch
                );
                batch.clear();
            }
        }
        if (!batch.isEmpty()) {
            jdbcTemplate.batchUpdate(
                "INSERT INTO players (username, email, mmr, region, created_at) VALUES (?,?,?,?,?)",
                batch
            );
        }
        log.info("Players seeded.");
    }

    private void seedMatchesBatch() {
        log.info("Seeding {} matches via JDBC batch...", matchCount);
        Random rng = new Random(42);

        // Récupère les IDs des joueurs
        List<Long> playerIds = jdbcTemplate.queryForList("SELECT id FROM players", Long.class);
        int pSize = playerIds.size();

        int batchSize = 500;
        List<Object[]> matchBatch = new ArrayList<>(batchSize);
        AtomicInteger processed = new AtomicInteger(0);

        for (int i = 0; i < matchCount; i++) {
            String gameMode = GAME_MODES[rng.nextInt(GAME_MODES.length)];
            String status = STATUSES[rng.nextInt(STATUSES.length)];
            String region = REGIONS[rng.nextInt(REGIONS.length)];
            int duration = 300 + rng.nextInt(3300);
            String serverId = "server-" + region + "-" + (1 + rng.nextInt(10));
            LocalDateTime created = LocalDateTime.now().minusDays(rng.nextInt(180))
                    .minusHours(rng.nextInt(24))
                    .minusMinutes(rng.nextInt(60));

            matchBatch.add(new Object[]{gameMode, status, duration, serverId, region, created});

            if (matchBatch.size() == batchSize || i == matchCount - 1) {
                int[][] keys = jdbcTemplate.batchUpdate(
                    "INSERT INTO matches (game_mode, status, duration_seconds, server_id, region, created_at) VALUES (?,?,?,?,?,?)",
                    matchBatch
                );

                // Récupère les IDs insérés pour les match_players
                List<Long> matchIds = jdbcTemplate.queryForList(
                    "SELECT id FROM matches ORDER BY id DESC LIMIT " + matchBatch.size(),
                    Long.class
                );

                // Insert match_players
                List<Object[]> mpBatch = new ArrayList<>();
                for (Long matchId : matchIds) {
                    int playersPerMatch = 2 + rng.nextInt(4); // 2 à 5 joueurs
                    for (int p = 0; p < playersPerMatch; p++) {
                        Long playerId = playerIds.get(rng.nextInt(pSize));
                        int score = rng.nextInt(10000);
                        String result = RESULTS[rng.nextInt(RESULTS.length)];
                        mpBatch.add(new Object[]{matchId, playerId, score, result});
                    }
                }
                jdbcTemplate.batchUpdate(
                    "INSERT INTO match_players (match_id, player_id, score, result) VALUES (?,?,?,?)",
                    mpBatch
                );

                matchBatch.clear();
                int done = processed.addAndGet(batchSize);
                if (done % 10000 == 0) {
                    log.info("  Seeded {}/{} matches...", done, matchCount);
                }
            }
        }
        log.info("Matches seeded.");
    }
}

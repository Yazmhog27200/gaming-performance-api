package com.gaming.api.service;

import com.gaming.api.dto.DashboardDTO;
import com.gaming.api.entity.Player;
import com.gaming.api.repository.MatchPlayerRepository;
import com.gaming.api.repository.MatchRepository;
import com.gaming.api.repository.PlayerRepository;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class DashboardService {

    private static final Logger log = LoggerFactory.getLogger(DashboardService.class);

    private final MatchRepository matchRepository;
    private final PlayerRepository playerRepository;
    private final MatchPlayerRepository matchPlayerRepository;
    private final PlayerService playerService;
    private final MeterRegistry meterRegistry;

    // ANTI-PATTERN: endpoint dashboard NON mis en cache
    // Cet endpoint est fortement sollicité (appelé par le frontend toutes les 5s)
    // Chaque appel exécute 8+ requêtes SQL lourdes + calculs Java
    // OPTIMISATION Jour 4 : @Cacheable(value="dashboard", key="'global'") avec TTL 10s
    @Transactional(readOnly = true)
    public DashboardDTO getDashboard() {
        Timer.Sample sample = Timer.start(meterRegistry);
        log.info("Building dashboard — NO CACHE — executing all queries...");

        try {
            // Stats plateforme (6 requêtes SQL)
            DashboardDTO.PlatformStatsDTO platformStats = buildPlatformStats();

            // Top 10 joueurs (1 requête SQL pour récupérer les joueurs par MMR)
            // ANTI-PATTERN N+1 : pour chaque joueur dans le top, calcule ses stats
            // = 10 appels à getPlayerStats() = 10 * (1 + N requêtes par joueur)
            List<DashboardDTO.TopPlayerDTO> topPlayers = buildTopPlayers();

            // Distribution par région (1 requête SQL)
            Map<String, Long> matchesByRegion = buildMatchesByRegion();

            // Distribution par mode de jeu (1 requête SQL)
            Map<String, Long> matchesByMode = buildMatchesByMode();

            // Health check DB
            DashboardDTO.HealthDTO health = buildHealthCheck();

            return new DashboardDTO(platformStats, topPlayers, matchesByRegion, matchesByMode, health);

        } finally {
            sample.stop(meterRegistry.timer("dashboard.build.time"));
        }
    }

    private DashboardDTO.PlatformStatsDTO buildPlatformStats() {
        long totalMatches = matchRepository.countTotal();
        long totalPlayers = playerRepository.countTotal();
        long activePlayers24h = playerRepository.countActiveSince(LocalDateTime.now().minusHours(24));
        Double avgDuration = matchRepository.averageDuration();
        long inProgress = matchRepository.countInProgress();
        long today = matchRepository.countSince(LocalDateTime.now().withHour(0).withMinute(0).withSecond(0));

        return new DashboardDTO.PlatformStatsDTO(
                totalMatches, totalPlayers, activePlayers24h,
                avgDuration != null ? avgDuration : 0.0,
                inProgress, today
        );
    }

    // ANTI-PATTERN N+1 MAJEUR :
    // 1 requête pour récupérer les top 10 joueurs
    // + pour CHAQUE joueur : playerService.getPlayerStats() = 1 requête Player + 1 requête MatchPlayer (tous les matchs)
    // = 1 + 10*2 = 21 requêtes SQL minimum pour 10 joueurs
    // Si chaque joueur a 500 matchs → charge 5000 entités en mémoire
    // OPTIMISATION Jour 4 : requête SQL directe avec JOIN et agrégation
    private List<DashboardDTO.TopPlayerDTO> buildTopPlayers() {
        List<Player> topPlayers = playerRepository.findTopByMmr(PageRequest.of(0, 10));

        return topPlayers.stream().map(player -> {
            // N+1 ici : un appel de stats complet par joueur
            try {
                var stats = playerService.getPlayerStats(player.getId());
                return new DashboardDTO.TopPlayerDTO(
                        player.getId(),
                        player.getUsername(),
                        player.getMmr(),
                        stats.getWinRate()
                );
            } catch (Exception e) {
                return new DashboardDTO.TopPlayerDTO(player.getId(), player.getUsername(), player.getMmr(), 0.0);
            }
        }).collect(Collectors.toList());
    }

    private Map<String, Long> buildMatchesByRegion() {
        List<Object[]> results = matchRepository.countByRegion();
        Map<String, Long> map = new LinkedHashMap<>();
        for (Object[] row : results) {
            map.put((String) row[0], (Long) row[1]);
        }
        return map;
    }

    private Map<String, Long> buildMatchesByMode() {
        List<Object[]> results = matchRepository.countByGameMode();
        Map<String, Long> map = new LinkedHashMap<>();
        for (Object[] row : results) {
            map.put((String) row[0], (Long) row[1]);
        }
        return map;
    }

    private DashboardDTO.HealthDTO buildHealthCheck() {
        long start = System.currentTimeMillis();
        // Simple ping DB
        matchRepository.countTotal();
        long dbMs = System.currentTimeMillis() - start;

        return new DashboardDTO.HealthDTO("UP", dbMs, -1);
    }
}

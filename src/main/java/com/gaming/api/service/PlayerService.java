package com.gaming.api.service;

import com.gaming.api.dto.PlayerStatsDTO;
import com.gaming.api.entity.Player;
import com.gaming.api.repository.MatchPlayerRepository;
import com.gaming.api.repository.PlayerRepository;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
public class PlayerService {

    private static final Logger log = LoggerFactory.getLogger(PlayerService.class);

    private final PlayerRepository playerRepository;
    private final MatchPlayerRepository matchPlayerRepository;
    private final MeterRegistry meterRegistry;

    @Transactional(readOnly = true)
    public Player getById(Long id) {
        return playerRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Player not found: " + id));
    }

    @Cacheable(value = "playerStats", key = "#playerId")
    @Transactional(readOnly = true)
    public PlayerStatsDTO getPlayerStats(Long playerId) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            List<Object[]> results = playerRepository.findAggregateStatsByPlayerId(playerId);
            if (results.isEmpty()) {
                throw new NoSuchElementException("Player not found: " + playerId);
            }
            Object[] row = results.get(0);
            long totalMatches = row[4] == null ? 0L : ((Number) row[4]).longValue();
            long wins        = row[5] == null ? 0L : ((Number) row[5]).longValue();
            long losses      = row[6] == null ? 0L : ((Number) row[6]).longValue();
            long draws       = row[7] == null ? 0L : ((Number) row[7]).longValue();
            double avgScore  = row[8] == null ? 0.0 : ((Number) row[8]).doubleValue();
            long totalTime   = row[9] == null ? 0L : ((Number) row[9]).longValue();
            double winRate   = totalMatches > 0 ? (double) wins / totalMatches * 100 : 0.0;

            return new PlayerStatsDTO(
                    ((Number) row[0]).longValue(),
                    (String) row[1],
                    (String) row[2],
                    row[3] == null ? null : ((Number) row[3]).intValue(),
                    totalMatches, wins, losses, draws, winRate, avgScore, totalTime
            );
        } finally {
            sample.stop(meterRegistry.timer("player.stats.computation"));
        }
    }

    @Transactional(readOnly = true)
    public List<Player> getTopPlayers(int limit) {
        return playerRepository.findTopByMmr(PageRequest.of(0, limit));
    }

    @Transactional
    public Player create(Player player) {
        return playerRepository.save(player);
    }
}

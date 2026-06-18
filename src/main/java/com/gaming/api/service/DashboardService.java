package com.gaming.api.service;

import com.gaming.api.dto.DashboardDTO;
import com.gaming.api.repository.MatchPlayerRepository;
import com.gaming.api.repository.MatchRepository;
import com.gaming.api.repository.PlayerRepository;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
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
    private final MeterRegistry meterRegistry;

    @Cacheable(value = "dashboard", key = "'global'")
    @Transactional(readOnly = true)
    public DashboardDTO getDashboard() {
        Timer.Sample sample = Timer.start(meterRegistry);
        log.info("Building dashboard (cache miss) — executing queries...");

        try {
            // Stats plateforme (6 requêtes SQL)
            DashboardDTO.PlatformStatsDTO platformStats = buildPlatformStats();

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

    private List<DashboardDTO.TopPlayerDTO> buildTopPlayers() {
        List<Object[]> rows = playerRepository.findTopPlayersWithWinRate();
        return rows.stream().map(row -> new DashboardDTO.TopPlayerDTO(
                ((Number) row[0]).longValue(),
                (String) row[1],
                row[2] == null ? 0 : ((Number) row[2]).intValue(),
                row[3] == null ? 0.0 : ((Number) row[3]).doubleValue() * 100
        )).collect(Collectors.toList());
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

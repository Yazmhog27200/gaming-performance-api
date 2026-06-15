package com.gaming.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DashboardDTO {
    private PlatformStatsDTO platformStats;
    private List<TopPlayerDTO> topPlayers;
    private Map<String, Long> matchesByRegion;
    private Map<String, Long> matchesByMode;
    private HealthDTO health;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PlatformStatsDTO {
        private Long totalMatches;
        private Long totalPlayers;
        private Long activePlayers24h;
        private Double averageMatchDuration;
        private Long matchesInProgress;
        private Long matchesToday;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class TopPlayerDTO {
        private Long playerId;
        private String username;
        private Integer mmr;
        private Double winRate;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class HealthDTO {
        private String status;
        private Long dbResponseMs;
        private Integer activeConnections;
    }
}

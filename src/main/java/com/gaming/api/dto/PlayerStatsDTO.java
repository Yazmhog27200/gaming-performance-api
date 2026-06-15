package com.gaming.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PlayerStatsDTO {
    private Long playerId;
    private String username;
    private String region;
    private Integer mmr;
    private Long totalMatches;
    private Long wins;
    private Long losses;
    private Long draws;
    private Double winRate;
    private Double averageScore;
    private Long totalPlayTimeSeconds;
}

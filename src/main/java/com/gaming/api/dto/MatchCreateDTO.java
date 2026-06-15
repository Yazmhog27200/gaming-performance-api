package com.gaming.api.dto;

import lombok.Data;

import java.util.List;

@Data
public class MatchCreateDTO {
    private String gameMode;
    private String status;
    private Integer durationSeconds;
    private String serverId;
    private String region;
    private List<PlayerEntry> players;

    @Data
    public static class PlayerEntry {
        private Long playerId;
        private Integer score;
        private String result;
    }
}

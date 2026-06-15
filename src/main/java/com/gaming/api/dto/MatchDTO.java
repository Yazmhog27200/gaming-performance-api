package com.gaming.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MatchDTO {
    private Long id;
    private String gameMode;
    private String status;
    private Integer durationSeconds;
    private String serverId;
    private String region;
    private LocalDateTime createdAt;
    private List<MatchPlayerDTO> players;

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MatchPlayerDTO {
        private Long playerId;
        private String username;
        private Integer score;
        private String result;
    }
}

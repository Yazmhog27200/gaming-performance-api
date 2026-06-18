package com.gaming.api.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "matches", indexes = {
    @Index(name = "idx_match_created_at", columnList = "created_at"),
    @Index(name = "idx_match_game_mode", columnList = "game_mode"),
    @Index(name = "idx_match_status", columnList = "status"),
    @Index(name = "idx_match_region", columnList = "region")
})
@Getter
@Setter
@NoArgsConstructor
public class Match {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "game_mode", nullable = false, length = 20)
    private String gameMode; // RANKED, CASUAL, TOURNAMENT

    @Column(name = "status", nullable = false, length = 20)
    private String status; // PENDING, IN_PROGRESS, FINISHED

    @Column(name = "duration_seconds")
    private Integer durationSeconds;

    @Column(name = "server_id", length = 50)
    private String serverId;

    @Column(name = "region", length = 20)
    private String region; // EU, NA, ASIA, SA

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @JsonIgnore
    @OneToMany(mappedBy = "match", fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    private List<MatchPlayer> matchPlayers = new ArrayList<>();

    @PrePersist
    public void prePersist() {
        this.createdAt = LocalDateTime.now();
    }
}

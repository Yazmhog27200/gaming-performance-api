package com.gaming.api.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "matches")
// ANTI-PATTERN: pas d'index sur created_at, game_mode, status, region
// Ces colonnes sont utilisées dans tous les filtres de recherche → full table scan sur 200k lignes
// OPTIMISATION Jour 4 : ajouter indexes={
//   @Index(name="idx_match_created_at", columnList="created_at"),
//   @Index(name="idx_match_game_mode", columnList="game_mode"),
//   @Index(name="idx_match_status", columnList="status"),
//   @Index(name="idx_match_region", columnList="region")
// }
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

    // ANTI-PATTERN: FetchType.EAGER — charge tous les MatchPlayer (et les Player associés)
    // à chaque fois qu'un Match est chargé, même pour un simple GET /matches/{id}
    // Génère des requêtes JOIN massives ou des N+1 selon le contexte
    // OPTIMISATION Jour 4 : FetchType.LAZY + @EntityGraph sur les requêtes qui en ont besoin
    @OneToMany(mappedBy = "match", fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
    private List<MatchPlayer> matchPlayers = new ArrayList<>();

    @PrePersist
    public void prePersist() {
        this.createdAt = LocalDateTime.now();
    }
}

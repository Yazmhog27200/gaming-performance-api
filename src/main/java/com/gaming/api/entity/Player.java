package com.gaming.api.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "players")
// ANTI-PATTERN: pas d'@Index sur username, region, mmr (colonnes filtrées fréquemment)
// OPTIMISATION Jour 4 : ajouter @Table(name="players", indexes={@Index(name="idx_player_username", columnList="username"), ...})
@Getter
@Setter
@NoArgsConstructor
public class Player {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "username", nullable = false, length = 50)
    private String username;

    @Column(name = "email", nullable = false, length = 100)
    private String email;

    @Column(name = "mmr")
    private Integer mmr = 1000;

    @Column(name = "region", length = 20)
    private String region;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // ANTI-PATTERN: FetchType.EAGER charge TOUS les matchs du joueur à chaque findById
    // Provoque des requêtes massives et inutiles quand on veut juste le profil du joueur
    // OPTIMISATION Jour 4 : passer à FetchType.LAZY
    @OneToMany(mappedBy = "player", fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    private List<MatchPlayer> matchPlayers = new ArrayList<>();

    @PrePersist
    public void prePersist() {
        this.createdAt = LocalDateTime.now();
    }
}

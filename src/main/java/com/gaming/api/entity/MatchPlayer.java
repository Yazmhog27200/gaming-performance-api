package com.gaming.api.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "match_players")
// ANTI-PATTERN: pas d'index composite sur (match_id, player_id)
// OPTIMISATION Jour 4 : @Table(indexes={@Index(columnList="match_id"), @Index(columnList="player_id")})
@Getter
@Setter
@NoArgsConstructor
public class MatchPlayer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // ANTI-PATTERN: FetchType.EAGER sur les deux côtés
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "match_id", nullable = false)
    private Match match;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "player_id", nullable = false)
    private Player player;

    @Column(name = "score")
    private Integer score = 0;

    @Column(name = "result", length = 10)
    private String result; // WIN, LOSS, DRAW

    public MatchPlayer(Match match, Player player, Integer score, String result) {
        this.match = match;
        this.player = player;
        this.score = score;
        this.result = result;
    }
}

package com.gaming.api.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = "match_players", indexes = {
    @Index(name = "idx_mp_match_id", columnList = "match_id"),
    @Index(name = "idx_mp_player_id", columnList = "player_id")
})
@Getter
@Setter
@NoArgsConstructor
public class MatchPlayer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "match_id", nullable = false)
    private Match match;

    @ManyToOne(fetch = FetchType.LAZY)
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

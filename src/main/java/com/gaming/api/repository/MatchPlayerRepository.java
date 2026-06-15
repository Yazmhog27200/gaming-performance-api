package com.gaming.api.repository;

import com.gaming.api.entity.MatchPlayer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MatchPlayerRepository extends JpaRepository<MatchPlayer, Long> {

    List<MatchPlayer> findByPlayerId(Long playerId);

    List<MatchPlayer> findByMatchId(Long matchId);

    @Query("SELECT mp FROM MatchPlayer mp WHERE mp.player.id = :playerId")
    List<MatchPlayer> findAllByPlayerId(@Param("playerId") Long playerId);

    @Query("SELECT COUNT(mp) FROM MatchPlayer mp WHERE mp.player.id = :playerId AND mp.result = :result")
    Long countByPlayerIdAndResult(@Param("playerId") Long playerId, @Param("result") String result);

    @Query("SELECT AVG(mp.score) FROM MatchPlayer mp WHERE mp.player.id = :playerId")
    Double averageScoreByPlayerId(@Param("playerId") Long playerId);

    // Pour les stats joueur — version optimisée avec projection SQL (Jour 4)
    @Query("""
        SELECT
            COUNT(mp) as totalMatches,
            SUM(CASE WHEN mp.result = 'WIN' THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN mp.result = 'LOSS' THEN 1 ELSE 0 END) as losses,
            SUM(CASE WHEN mp.result = 'DRAW' THEN 1 ELSE 0 END) as draws,
            AVG(mp.score) as avgScore,
            SUM(mp.match.durationSeconds) as totalPlayTime
        FROM MatchPlayer mp
        WHERE mp.player.id = :playerId
    """)
    Object[] getPlayerAggregateStats(@Param("playerId") Long playerId);
}

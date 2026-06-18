package com.gaming.api.repository;

import com.gaming.api.entity.Player;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface PlayerRepository extends JpaRepository<Player, Long> {

    Optional<Player> findByUsername(String username);

    List<Player> findByRegion(String region);

    // Top joueurs par MMR (pour le dashboard)
    @Query("SELECT p FROM Player p ORDER BY p.mmr DESC")
    List<Player> findTopByMmr(Pageable pageable);

    // Joueurs actifs dans les dernières N heures
    @Query("SELECT DISTINCT mp.player FROM MatchPlayer mp WHERE mp.match.createdAt >= :since")
    List<Player> findActiveSince(@Param("since") LocalDateTime since);

    @Query("SELECT COUNT(DISTINCT mp.player) FROM MatchPlayer mp WHERE mp.match.createdAt >= :since")
    Long countActiveSince(@Param("since") LocalDateTime since);

    @Query("SELECT COUNT(p) FROM Player p")
    Long countTotal();

    @Query("""
        SELECT p.id, p.username, p.region, p.mmr,
               COUNT(mp),
               SUM(CASE WHEN mp.result = 'WIN' THEN 1 ELSE 0 END),
               SUM(CASE WHEN mp.result = 'LOSS' THEN 1 ELSE 0 END),
               SUM(CASE WHEN mp.result = 'DRAW' THEN 1 ELSE 0 END),
               AVG(mp.score),
               SUM(mp.match.durationSeconds)
        FROM Player p
        LEFT JOIN p.matchPlayers mp
        WHERE p.id = :playerId
        GROUP BY p.id, p.username, p.region, p.mmr
        """)
    List<Object[]> findAggregateStatsByPlayerId(@Param("playerId") Long playerId);

    @Query(value = """
        SELECT p.id, p.username, p.mmr,
               CAST(COALESCE(SUM(CASE WHEN mp.result = 'WIN' THEN 1.0 ELSE 0.0 END), 0) AS float)
               / NULLIF(COUNT(mp.id), 0)
        FROM players p
        LEFT JOIN match_players mp ON mp.player_id = p.id
        GROUP BY p.id, p.username, p.mmr
        ORDER BY p.mmr DESC
        LIMIT 10
        """, nativeQuery = true)
    List<Object[]> findTopPlayersWithWinRate();
}

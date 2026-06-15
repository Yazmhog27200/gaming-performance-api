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
}

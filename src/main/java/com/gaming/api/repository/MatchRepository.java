package com.gaming.api.repository;

import com.gaming.api.entity.Match;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface MatchRepository extends JpaRepository<Match, Long> {

    // Requête initiale non optimisée (charge toutes les entités + EAGER)
    List<Match> findByGameMode(String gameMode);

    List<Match> findByStatus(String status);

    List<Match> findByRegion(String region);

    List<Match> findByCreatedAtBetween(LocalDateTime from, LocalDateTime to);

    // Recherche multi-critères JPQL (sans pagination SQL — anti-pattern résolu en Jour 4)
    @Query("SELECT m FROM Match m WHERE " +
           "(:gameMode IS NULL OR m.gameMode = :gameMode) AND " +
           "(:status IS NULL OR m.status = :status) AND " +
           "(:region IS NULL OR m.region = :region) AND " +
           "(:from IS NULL OR m.createdAt >= :from) AND " +
           "(:to IS NULL OR m.createdAt <= :to)")
    List<Match> searchMatches(
            @Param("gameMode") String gameMode,
            @Param("status") String status,
            @Param("region") String region,
            @Param("from") LocalDateTime from,
            @Param("to") LocalDateTime to
    );

    // Version optimisée avec pagination SQL (Jour 4)
    @Query("SELECT m FROM Match m WHERE " +
           "(:gameMode IS NULL OR m.gameMode = :gameMode) AND " +
           "(:status IS NULL OR m.status = :status) AND " +
           "(:region IS NULL OR m.region = :region) AND " +
           "(:from IS NULL OR m.createdAt >= :from) AND " +
           "(:to IS NULL OR m.createdAt <= :to)")
    Page<Match> searchMatchesPaged(
            @Param("gameMode") String gameMode,
            @Param("status") String status,
            @Param("region") String region,
            @Param("from") LocalDateTime from,
            @Param("to") LocalDateTime to,
            Pageable pageable
    );

    // Stats pour dashboard
    @Query("SELECT COUNT(m) FROM Match m")
    Long countTotal();

    @Query("SELECT COUNT(m) FROM Match m WHERE m.status = 'IN_PROGRESS'")
    Long countInProgress();

    @Query("SELECT COUNT(m) FROM Match m WHERE m.createdAt >= :since")
    Long countSince(@Param("since") LocalDateTime since);

    @Query("SELECT AVG(m.durationSeconds) FROM Match m WHERE m.status = 'FINISHED'")
    Double averageDuration();

    @Query("SELECT m.region, COUNT(m) FROM Match m GROUP BY m.region")
    List<Object[]> countByRegion();

    @Query("SELECT m.gameMode, COUNT(m) FROM Match m GROUP BY m.gameMode")
    List<Object[]> countByGameMode();
}

package com.gaming.api.service;

import com.gaming.api.dto.PlayerStatsDTO;
import com.gaming.api.entity.MatchPlayer;
import com.gaming.api.entity.Player;
import com.gaming.api.repository.MatchPlayerRepository;
import com.gaming.api.repository.PlayerRepository;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.NoSuchElementException;

@Service
@RequiredArgsConstructor
public class PlayerService {

    private static final Logger log = LoggerFactory.getLogger(PlayerService.class);

    private final PlayerRepository playerRepository;
    private final MatchPlayerRepository matchPlayerRepository;
    private final MeterRegistry meterRegistry;

    @Transactional(readOnly = true)
    public Player getById(Long id) {
        return playerRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Player not found: " + id));
    }

    // ANTI-PATTERN: calcul des statistiques via chargement complet des entités en mémoire
    // Pour un joueur avec 500 matchs : charge 500 MatchPlayer + 500 Match + 500*N Player
    // Complexité temporelle O(n) en Java au lieu d'un COUNT/SUM/AVG SQL en O(log n)
    // OPTIMISATION Jour 4 : utiliser getPlayerAggregateStats() du repository (une seule requête SQL)
    @Transactional(readOnly = true)
    public PlayerStatsDTO getPlayerStats(Long playerId) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            Player player = playerRepository.findById(playerId)
                    .orElseThrow(() -> new NoSuchElementException("Player not found: " + playerId));

            // ANTI-PATTERN: chargement de toutes les participations pour calculer en Java
            List<MatchPlayer> participations = matchPlayerRepository.findAllByPlayerId(playerId);

            log.debug("Loaded {} match participations for player {} — computing stats in Java", participations.size(), playerId);

            long totalMatches = participations.size();
            long wins = participations.stream().filter(mp -> "WIN".equals(mp.getResult())).count();
            long losses = participations.stream().filter(mp -> "LOSS".equals(mp.getResult())).count();
            long draws = participations.stream().filter(mp -> "DRAW".equals(mp.getResult())).count();
            double avgScore = participations.stream()
                    .mapToInt(mp -> mp.getScore() != null ? mp.getScore() : 0)
                    .average().orElse(0.0);
            // ANTI-PATTERN: chargement du Match complet pour accéder à durationSeconds
            long totalPlayTime = participations.stream()
                    .mapToLong(mp -> mp.getMatch().getDurationSeconds() != null ? mp.getMatch().getDurationSeconds() : 0)
                    .sum();
            double winRate = totalMatches > 0 ? (double) wins / totalMatches * 100 : 0.0;

            return new PlayerStatsDTO(
                    player.getId(),
                    player.getUsername(),
                    player.getRegion(),
                    player.getMmr(),
                    totalMatches,
                    wins,
                    losses,
                    draws,
                    winRate,
                    avgScore,
                    totalPlayTime
            );
        } finally {
            sample.stop(meterRegistry.timer("player.stats.computation"));
        }
    }

    @Transactional(readOnly = true)
    public List<Player> getTopPlayers(int limit) {
        return playerRepository.findTopByMmr(PageRequest.of(0, limit));
    }

    @Transactional
    public Player create(Player player) {
        return playerRepository.save(player);
    }
}

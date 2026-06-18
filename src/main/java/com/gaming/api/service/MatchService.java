package com.gaming.api.service;

import com.gaming.api.dto.MatchCreateDTO;
import com.gaming.api.dto.MatchDTO;
import com.gaming.api.entity.Match;
import com.gaming.api.entity.MatchPlayer;
import com.gaming.api.entity.Player;
import com.gaming.api.kafka.MatchEventProducer;
import com.gaming.api.repository.MatchPlayerRepository;
import com.gaming.api.repository.MatchRepository;
import com.gaming.api.repository.PlayerRepository;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class MatchService {

    private static final Logger log = LoggerFactory.getLogger(MatchService.class);

    private final MatchRepository matchRepository;
    private final PlayerRepository playerRepository;
    private final MatchPlayerRepository matchPlayerRepository;
    private final MatchEventProducer matchEventProducer;
    private final MeterRegistry meterRegistry;

    @Transactional(readOnly = true)
    public MatchDTO getById(Long id) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            Match match = matchRepository.findById(id)
                    .orElseThrow(() -> new NoSuchElementException("Match not found: " + id));
            return toDTO(match);
        } finally {
            sample.stop(meterRegistry.timer("match.get.by.id"));
        }
    }

    @Transactional(readOnly = true)
    public List<MatchDTO> getAll(int page, int size) {
        return matchRepository.findAll(PageRequest.of(page, size)).stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public List<MatchDTO> search(String gameMode, String status, String region,
                                  LocalDateTime from, LocalDateTime to) {
        // ANTI-PATTERN: pas de pagination — peut retourner des milliers de résultats
        List<Match> matches = matchRepository.searchMatches(gameMode, status, region, from, to);
        return matches.stream().map(this::toDTO).collect(Collectors.toList());
    }

    @Transactional
    public MatchDTO create(MatchCreateDTO dto) {
        Counter.builder("match.created").register(meterRegistry).increment();

        Match match = new Match();
        match.setGameMode(dto.getGameMode());
        match.setStatus(dto.getStatus() != null ? dto.getStatus() : "PENDING");
        match.setDurationSeconds(dto.getDurationSeconds());
        match.setServerId(dto.getServerId());
        match.setRegion(dto.getRegion());

        Match saved = matchRepository.save(match);

        if (dto.getPlayers() != null) {
            for (MatchCreateDTO.PlayerEntry entry : dto.getPlayers()) {
                // ANTI-PATTERN N+1 : un findById par joueur dans une boucle
                Player player = playerRepository.findById(entry.getPlayerId())
                        .orElseThrow(() -> new NoSuchElementException("Player not found: " + entry.getPlayerId()));
                MatchPlayer mp = new MatchPlayer(saved, player, entry.getScore(), entry.getResult());
                matchPlayerRepository.save(mp); // ANTI-PATTERN: sauvegarde un par un, pas en batch
            }
        }

        // Événement Kafka async
        matchEventProducer.sendMatchCreated(saved.getId(), saved.getGameMode(), saved.getRegion());

        return toDTO(matchRepository.findById(saved.getId()).orElseThrow());
    }

    @Transactional
    public MatchDTO updateStatus(Long id, String status) {
        Match match = matchRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Match not found: " + id));
        match.setStatus(status);
        return toDTO(matchRepository.save(match));
    }

    // ANTI-PATTERN: mapping dans le service (acceptable) mais sans projection DTO
    // Charge toutes les données de l'entité même si on n'en a pas besoin
    // OPTIMISATION Jour 4 : utiliser des projections JPA interface ou JPQL DTO constructor
    private MatchDTO toDTO(Match match) {
        List<MatchDTO.MatchPlayerDTO> players = match.getMatchPlayers().stream()
                .map(mp -> new MatchDTO.MatchPlayerDTO(
                        mp.getPlayer().getId(),
                        mp.getPlayer().getUsername(),
                        mp.getScore(),
                        mp.getResult()
                ))
                .collect(Collectors.toList());

        return new MatchDTO(
                match.getId(),
                match.getGameMode(),
                match.getStatus(),
                match.getDurationSeconds(),
                match.getServerId(),
                match.getRegion(),
                match.getCreatedAt(),
                players
        );
    }
}

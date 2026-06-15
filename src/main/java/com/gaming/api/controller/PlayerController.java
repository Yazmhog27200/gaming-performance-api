package com.gaming.api.controller;

import com.gaming.api.dto.PlayerStatsDTO;
import com.gaming.api.entity.Player;
import com.gaming.api.service.PlayerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/players")
@RequiredArgsConstructor
public class PlayerController {

    private final PlayerService playerService;

    @GetMapping("/{id}")
    public ResponseEntity<Player> getById(@PathVariable Long id) {
        return ResponseEntity.ok(playerService.getById(id));
    }

    @GetMapping("/{id}/stats")
    public ResponseEntity<PlayerStatsDTO> getStats(@PathVariable Long id) {
        return ResponseEntity.ok(playerService.getPlayerStats(id));
    }

    @GetMapping("/top")
    public ResponseEntity<List<Player>> getTop(@RequestParam(defaultValue = "10") int limit) {
        return ResponseEntity.ok(playerService.getTopPlayers(limit));
    }

    @PostMapping
    public ResponseEntity<Player> create(@RequestBody Player player) {
        return ResponseEntity.ok(playerService.create(player));
    }
}

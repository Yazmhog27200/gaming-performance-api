package com.gaming.api.controller;

import com.gaming.api.dto.MatchCreateDTO;
import com.gaming.api.dto.MatchDTO;
import com.gaming.api.service.MatchService;
import lombok.RequiredArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/matches")
@RequiredArgsConstructor
public class MatchController {

    private final MatchService matchService;

    @GetMapping("/{id}")
    public ResponseEntity<MatchDTO> getById(@PathVariable Long id) {
        return ResponseEntity.ok(matchService.getById(id));
    }

    @GetMapping
    public ResponseEntity<List<MatchDTO>> getAll(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        // ANTI-PATTERN: pagination côté Java dans le service
        return ResponseEntity.ok(matchService.getAll(page, size));
    }

    @GetMapping("/search")
    public ResponseEntity<List<MatchDTO>> search(
            @RequestParam(required = false) String gameMode,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String region,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime from,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime to) {
        return ResponseEntity.ok(matchService.search(gameMode, status, region, from, to));
    }

    @PostMapping
    public ResponseEntity<MatchDTO> create(@RequestBody MatchCreateDTO dto) {
        return ResponseEntity.accepted().body(matchService.create(dto));
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<MatchDTO> updateStatus(
            @PathVariable Long id,
            @RequestParam String status) {
        return ResponseEntity.ok(matchService.updateStatus(id, status));
    }
}

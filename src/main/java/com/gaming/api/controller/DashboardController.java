package com.gaming.api.controller;

import com.gaming.api.dto.DashboardDTO;
import com.gaming.api.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;

    // Endpoint le plus sollicité — appelé par tous les clients en temps réel
    // ANTI-PATTERN: aucun cache, recalcul à chaque requête
    @GetMapping("/dashboard")
    public ResponseEntity<DashboardDTO> getDashboard() {
        return ResponseEntity.ok(dashboardService.getDashboard());
    }
}

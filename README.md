# Gaming Performance API

API REST Spring Boot pour une plateforme de jeu vidéo compétitif en ligne.  
Projet axé sur l'**optimisation des performances backend** : monitoring, tests de charge, analyse des goulets d'étranglement et mise en place d'optimisations mesurables.

---

## Stack technique

| Catégorie | Technologie |
|---|---|
| Langage | Java 17 |
| Framework | Spring Boot 3.3 |
| Build | Maven |
| Base de données | PostgreSQL 16 |
| ORM | JPA / Hibernate |
| Monitoring | Micrometer + Prometheus |
| Visualisation | Grafana |
| Messaging | Apache Kafka |
| Load testing | Apache JMeter |
| Infrastructure | Docker / Docker Compose |

---

## Contexte

Plateforme backend gérant les matchs d'un jeu compétitif en ligne.  
L'API supporte une montée en charge progressive et expose des métriques techniques pour l'analyse des performances.

**Fonctionnalités :**
- Enregistrement et consultation des parties (matchs, joueurs, scores)
- Recherche et filtrage multi-critères (mode de jeu, région, statut, date)
- Statistiques joueurs : taux de victoire, score moyen, MMR/ELO, temps de jeu
- KPIs plateforme : parties jouées, joueurs actifs, durée moyenne, charge serveur
- Endpoint `/api/dashboard` — agrégation temps réel des indicateurs clés
- Architecture event-driven via Kafka (création de match → event → consumer async)

---

## Architecture

```
Client
  └── GET/POST /api/**
        └── Spring Boot (port 8080)
              ├── MatchController / PlayerController / DashboardController
              ├── Service Layer (logique métier)
              ├── Repository Layer (JPA / PostgreSQL)
              └── Kafka Producer → Topic match-events → Kafka Consumer

Monitoring :
  Spring Boot Actuator /actuator/prometheus
        └── Prometheus (port 9090)
              └── Grafana (port 3000)
```

---

## Lancer le projet

### Prérequis

- Docker Desktop installé et démarré
- Java 17+ (pour développement local)
- Maven 3.8+

### Démarrage complet via Docker Compose

```bash
git clone <url-du-depot>
cd gaming-performance-api

docker compose up -d
```

Les services démarrent dans l'ordre :
1. PostgreSQL → initialisation de la base
2. Kafka + ZooKeeper
3. Application Spring Boot (seed automatique : 10 000 joueurs + 200 000 matchs)
4. Prometheus + Grafana

### Accès

| Service | URL | Credentials |
|---|---|---|
| API REST | http://localhost:8080 | — |
| Actuator / Métriques | http://localhost:8080/actuator/prometheus | — |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |
| Kafka UI | http://localhost:8090 | — |

---

## Endpoints API

### Matchs

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/api/matches?page=0&size=20` | Liste paginée des matchs |
| `GET` | `/api/matches/{id}` | Détail d'un match |
| `GET` | `/api/matches/search?gameMode=RANKED&region=EU` | Recherche filtrée |
| `POST` | `/api/matches` | Créer un match |
| `PATCH` | `/api/matches/{id}/status?status=FINISHED` | Mettre à jour le statut |

### Joueurs

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/api/players/{id}` | Profil joueur |
| `GET` | `/api/players/{id}/stats` | Statistiques joueur |
| `GET` | `/api/players/top?limit=10` | Top joueurs par MMR |
| `POST` | `/api/players` | Créer un joueur |

### Dashboard

| Méthode | Endpoint | Description |
|---|---|---|
| `GET` | `/api/dashboard` | KPIs plateforme + top joueurs |

### Exemple de création de match

```json
POST /api/matches
{
  "gameMode": "RANKED",
  "status": "FINISHED",
  "durationSeconds": 1800,
  "serverId": "server-EU-3",
  "region": "EU",
  "players": [
    { "playerId": 1, "score": 8500, "result": "WIN" },
    { "playerId": 2, "score": 6200, "result": "LOSS" },
    { "playerId": 3, "score": 5900, "result": "LOSS" }
  ]
}
```

---

## Tests de charge — JMeter

3 scénarios disponibles dans le dossier `jmeter/` :

| Fichier | Scénario | Threads | Durée |
|---|---|---|---|
| `01-scenario-lecture-massive.jmx` | Lectures massives (GET) | 100 | 3 min |
| `02-scenario-ecriture-concurrente.jmx` | Écritures concurrentes (POST) | 50 | 2 min |
| `03-scenario-mixte.jmx` | Mixte 70% lecture / 30% écriture | 200 | 5 min |

### Lancer un test

```bash
# Mode ligne de commande (recommandé pour les gros tests)
jmeter -n -t jmeter/01-scenario-lecture-massive.jmx -l jmeter/results/result.jtl

# Générer un rapport HTML
jmeter -g jmeter/results/result.jtl -o jmeter/results/report/
```

---

## Monitoring — Grafana

Le dashboard est provisionné automatiquement au démarrage.

**Métriques disponibles :**
- Temps de réponse HTTP : p50 / p95 / p99 par endpoint
- Throughput (req/s)
- CPU JVM (process + system)
- Mémoire JVM : heap / non-heap
- Threads JVM (live, daemon, bloqués)
- GC pause rate
- HikariCP : connexions actives / idle / en attente
- Métriques métier : dashboard build time, stats computation time, events Kafka

---

## Anti-patterns identifiés (architecture initiale)

L'architecture de départ est **volontairement non optimisée** pour permettre l'analyse et la mesure des impacts.

| Anti-pattern | Localisation | Impact |
|---|---|---|
| `FetchType.EAGER` sur toutes les relations | `Match.java`, `Player.java`, `MatchPlayer.java` | Chargement inutile de données en mémoire |
| Pagination côté Java | `MatchService.getAll()` | `findAll()` charge 200 000 lignes en mémoire |
| N+1 queries | `DashboardService.buildTopPlayers()` | 1 + N×2 requêtes SQL par appel dashboard |
| Aucun cache sur `/api/dashboard` | `DashboardService.getDashboard()` | Recalcul complet à chaque requête |
| Stats calculées en Java | `PlayerService.getPlayerStats()` | Chargement de toutes les entités au lieu d'un `COUNT/SUM/AVG` SQL |
| Absence d'index SQL | Toutes les entités | Full table scan sur chaque filtre |
| Sauvegarde un par un | `MatchService.create()` | N inserts séparés au lieu d'un batch |

---

## Optimisations appliquées (Jour 4)

- Index SQL sur les colonnes filtrées (`created_at`, `game_mode`, `status`, `region`)
- `FetchType.LAZY` + `@EntityGraph` ciblé
- Pagination SQL via `Pageable` Spring Data
- Cache Caffeine sur `/api/dashboard` (TTL 10s) et statistiques joueur (TTL 60s)
- Requête SQL agrégée pour les stats joueur (une seule requête vs N)
- Pool HikariCP dimensionné selon la charge mesurée
- DTOs / projections JPA en lieu et place des entités complètes

---

## Structure du projet

```
gaming-performance-api/
├── docker-compose.yml
├── Dockerfile
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   └── dashboards/
│   └── dashboards/
│       └── gaming-api-dashboard.json
├── jmeter/
│   ├── 01-scenario-lecture-massive.jmx
│   ├── 02-scenario-ecriture-concurrente.jmx
│   └── 03-scenario-mixte.jmx
└── src/main/java/com/gaming/api/
    ├── entity/         (Match, Player, MatchPlayer)
    ├── repository/     (JPA Repositories)
    ├── service/        (MatchService, PlayerService, DashboardService)
    ├── controller/     (REST Controllers)
    ├── dto/            (MatchDTO, PlayerStatsDTO, DashboardDTO)
    ├── kafka/          (MatchEventProducer, MatchEventConsumer)
    └── config/         (DataSeeder)
```

---

## Données de test

Au premier démarrage, l'application insère automatiquement :
- **10 000 joueurs** répartis sur 4 régions (EU, NA, ASIA, SA) avec MMR aléatoire
- **200 000 matchs** sur les 6 derniers mois (modes RANKED, CASUAL, TOURNAMENT)
- **~700 000 entrées `match_players`** (2 à 5 joueurs par match)

Pour désactiver le seed : `app.seed.enabled=false` dans `application.yml`.

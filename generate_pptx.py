from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

DARK   = RGBColor(0x12, 0x12, 0x2B)
BLUE   = RGBColor(0x1A, 0x4F, 0x8A)
ORANGE = RGBColor(0xF0, 0x6A, 0x1A)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GREY   = RGBColor(0xCC, 0xCC, 0xCC)
GREEN  = RGBColor(0x2E, 0xCC, 0x71)
RED    = RGBColor(0xE7, 0x4C, 0x3C)
YELLOW = RGBColor(0xF1, 0xC4, 0x0F)
LBLUE  = RGBColor(0x1A, 0x8C, 0xD8)
PURPLE = RGBColor(0x8E, 0x44, 0xAD)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def bg(slide, color=DARK):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = color

def box(slide, l, t, w, h, color):
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    s.line.fill.background()
    s.fill.solid()
    s.fill.fore_color.rgb = color
    return s

def txt(slide, text, l, t, w, h, size=22, bold=False, color=WHITE, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color

def stripe(slide):
    box(slide, 0, 0, 13.33, 0.45, BLUE)
    box(slide, 0, 7.05, 13.33, 0.45, BLUE)

def speaker(slide, who, color=ORANGE):
    box(slide, 11.5, 0.08, 1.7, 0.3, color)
    txt(slide, who, 11.52, 0.09, 1.66, 0.28, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

def pill(slide, label, l, t, color=BLUE):
    box(slide, l, t, 1.9, 0.38, color)
    txt(slide, label, l, t+0.05, 1.9, 0.3, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ───────────────────────────────────────────────
# SLIDE 1 — TITRE
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s)
box(s, 0, 3.0, 13.33, 0.1, ORANGE)

txt(s, "🎮", 0, 0.5, 13.33, 1.3, size=72, align=PP_ALIGN.CENTER)
txt(s, "OPTIMISATION DES PERFORMANCES", 0, 1.8, 13.33, 0.8,
    size=30, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
txt(s, "d'une API Gaming — Architecture complète", 0, 2.55, 13.33, 0.55,
    size=22, color=WHITE, align=PP_ALIGN.CENTER)

txt(s, "Spring Boot  ·  PostgreSQL  ·  Kafka  ·  Prometheus  ·  Grafana  ·  Spring Cloud Gateway",
    0, 3.3, 13.33, 0.45, size=14, color=GREY, align=PP_ALIGN.CENTER)

roles = [
    ("Nicolas", "Gateway",    BLUE),
    ("Jovany",  "JMeter",     PURPLE),
    ("hyppo",   "Grafana",    GREEN),
    ("Dilou",   "Prometheus", RGBColor(0xF3,0x9C,0x12)),
    ("Nassim",  "Kafka",      RED),
]
for i, (name, role, col) in enumerate(roles):
    l = 0.8 + i * 2.37
    box(s, l, 4.05, 2.2, 0.9, col)
    txt(s, name, l, 4.1,  2.2, 0.42, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, role, l, 4.55, 2.2, 0.38, size=13, color=WHITE, align=PP_ALIGN.CENTER)

txt(s, "Groupe — 2026", 0, 6.9, 13.33, 0.4, size=13, color=GREY, align=PP_ALIGN.CENTER)

# ───────────────────────────────────────────────
# SLIDE 2 — ARCHITECTURE GLOBALE
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Tous")

txt(s, "Architecture du Projet", 0.5, 0.55, 12, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)

# Flux principal
nodes = [
    ("🌐", "CLIENT",          "Navigateur / JMeter",   BLUE,   0.4),
    ("🔀", "GATEWAY",         ":8080\nRouting + CORS",  ORANGE, 3.1),
    ("⚙️", "API",             ":8081\nSpring Boot",     BLUE,   5.8),
    ("🗄️", "PostgreSQL",      ":5432\n200k matchs",     RGBColor(0x27,0x6E,0xA0), 8.5),
]
for icon, title, sub, col, l in nodes:
    box(s, l, 1.35, 2.5, 2.4, col)
    txt(s, icon,  l, 1.45, 2.5, 0.85, size=36, align=PP_ALIGN.CENTER)
    txt(s, title, l, 2.3,  2.5, 0.55, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, sub,   l, 2.85, 2.5, 0.65, size=12, color=WHITE, align=PP_ALIGN.CENTER)

for lx in [2.92, 5.62, 8.32]:
    txt(s, "→", lx, 2.3, 0.35, 0.5, size=22, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

# Kafka séparé (branché sur l'API)
box(s, 8.5, 4.1, 2.5, 1.6, RED)
txt(s, "📨 KAFKA", 8.5, 4.18, 2.5, 0.5, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, ":29092\nmatch-events", 8.5, 4.68, 2.5, 0.6, size=12, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "↕", 9.6, 3.77, 0.35, 0.38, size=18, bold=True, color=RED, align=PP_ALIGN.CENTER)

# Monitoring
box(s, 0.4, 4.1, 2.5, 1.6, PURPLE)
txt(s, "📡 PROMETHEUS", 0.4, 4.18, 2.5, 0.5, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, ":9090\nScrape toutes les 10s", 0.4, 4.68, 2.5, 0.6, size=11, color=WHITE, align=PP_ALIGN.CENTER)

box(s, 3.1, 4.1, 2.5, 1.6, GREEN)
txt(s, "📊 GRAFANA", 3.1, 4.18, 2.5, 0.5, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, ":3000\nDashboards", 3.1, 4.68, 2.5, 0.6, size=12, color=WHITE, align=PP_ALIGN.CENTER)

txt(s, "→", 2.92, 4.6, 0.25, 0.4, size=18, bold=True, color=GREY, align=PP_ALIGN.CENTER)
txt(s, "↑  scrape", 0.9, 3.78, 2.5, 0.38, size=11, color=GREY, align=PP_ALIGN.CENTER)

# Ports résumé
box(s, 0.4, 6.05, 12.3, 0.7, RGBColor(0x1A,0x1A,0x3E))
ports = [
    (":8080 Gateway", ORANGE),
    (":8081 API directe", BLUE),
    (":3000 Grafana", GREEN),
    (":9090 Prometheus", PURPLE),
    (":8090 Kafka UI", RED),
]
for i, (label, col) in enumerate(ports):
    pill(s, label, 0.55 + i*2.42, 6.18, col)

# ───────────────────────────────────────────────
# SLIDE 3 — GATEWAY (Nicolas)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Nicolas")

txt(s, "Spring Cloud Gateway", 0.5, 0.55, 11, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "Point d'entrée unique — tout le trafic passe par là avant d'arriver à l'API",
    0.7, 1.25, 12, 0.4, size=16, color=GREY)

# Schéma routing
box(s, 0.5, 1.8, 2.8, 1.5, BLUE)
txt(s, "🌐 CLIENT", 0.5, 1.9, 2.8, 0.55, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "localhost:8080", 0.5, 2.45, 2.8, 0.4, size=13, color=GREY, align=PP_ALIGN.CENTER)

txt(s, "→", 3.35, 2.3, 0.5, 0.5, size=26, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

box(s, 3.9, 1.8, 3.2, 1.5, ORANGE)
txt(s, "🔀 GATEWAY", 3.9, 1.9, 3.2, 0.55, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "Routing · CORS · Headers", 3.9, 2.45, 3.2, 0.4, size=12, color=WHITE, align=PP_ALIGN.CENTER)

txt(s, "→", 7.15, 2.3, 0.5, 0.5, size=26, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

box(s, 7.7, 1.8, 2.8, 1.5, BLUE)
txt(s, "⚙️ API", 7.7, 1.9, 2.8, 0.55, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "gaming-api:8080", 7.7, 2.45, 2.8, 0.4, size=13, color=GREY, align=PP_ALIGN.CENTER)

# Ce que la gateway fait concrètement
features = [
    ("🔁", "Routing",           "/api/** → gaming-api:8081\nUn seul port exposé au client"),
    ("📋", "Headers ajoutés",   "X-Gateway-Source: gaming-gateway\nX-Served-By: gaming-gateway"),
    ("🌍", "CORS centralisé",   "Configuré une seule fois\npour toute l'API"),
    ("📡", "Métriques propres", "spring_cloud_gateway_requests\nVisibles dans Prometheus"),
]
for i, (icon, title, desc) in enumerate(features):
    l = 0.5 + i * 3.15
    box(s, l, 3.65, 2.95, 2.05, RGBColor(0x1A,0x1A,0x3E))
    txt(s, icon,  l,      3.72, 2.95, 0.7,  size=28, align=PP_ALIGN.CENTER)
    txt(s, title, l,      4.42, 2.95, 0.5,  size=14, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    txt(s, desc,  l,      4.92, 2.95, 0.65, size=12, color=GREY, align=PP_ALIGN.CENTER)

box(s, 0.5, 5.95, 12.3, 0.8, RGBColor(0x0D,0x1A,0x0D))
txt(s, "Preuve en direct :", 0.75, 6.02, 3.5, 0.35, size=13, bold=True, color=GREEN)
txt(s, 'curl -s -D - -o /dev/null http://localhost:8080/api/dashboard | grep X-Served-By',
    0.75, 6.4, 12.0, 0.3, size=12, color=LBLUE)

# ───────────────────────────────────────────────
# SLIDE 4 — JMETER (Jovany)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Jovany")

txt(s, "JMeter — Tests de Charge", 0.5, 0.55, 11, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "Simule des centaines d'utilisateurs en même temps — c'est ce qui fait bouger Grafana",
    0.7, 1.25, 12, 0.4, size=16, color=GREY)

scenarios = [
    ("📖", "LECTURE\nMASSIVE",       "100 utilisateurs\n3 minutes",   "GET /api/matches\nGET /api/dashboard", BLUE,   "01-scenario-lecture-massive.jmx"),
    ("✍️",  "ÉCRITURE\nCONCURRENTE", "50 utilisateurs\n2 minutes",    "POST /api/matches\ncréation en masse", PURPLE, "02-scenario-ecriture-concurrente.jmx"),
    ("🔀", "SCÉNARIO\nMIXTE",        "200 utilisateurs\n5 minutes",   "70% lecture\n30% écriture",            RGBColor(0xF3,0x9C,0x12), "03-scenario-mixte.jmx"),
]
for i, (icon, title, params, desc, col, fname) in enumerate(scenarios):
    l = 0.5 + i * 4.2
    box(s, l, 1.8, 3.95, 3.8, col)
    txt(s, icon,   l, 1.9,  3.95, 1.0,  size=44, align=PP_ALIGN.CENTER)
    txt(s, title,  l, 2.9,  3.95, 0.75, size=18, bold=True, color=WHITE,  align=PP_ALIGN.CENTER)
    txt(s, params, l, 3.68, 3.95, 0.55, size=14, bold=True, color=YELLOW, align=PP_ALIGN.CENTER)
    txt(s, desc,   l, 4.28, 3.95, 0.65, size=13, color=WHITE, align=PP_ALIGN.CENTER)
    box(s, l, 5.63, 3.95, 0.3, RGBColor(0x0D,0x0D,0x1E))
    txt(s, fname,  l, 5.65, 3.95, 0.28, size=10, color=GREY, align=PP_ALIGN.CENTER)

box(s, 0.5, 6.1, 12.3, 0.85, RGBColor(0x0D,0x1A,0x0D))
txt(s, "Lancer le test :", 0.75, 6.17, 3.5, 0.35, size=13, bold=True, color=GREEN)
txt(s, "jmeter -n -t jmeter/03-scenario-mixte.jmx -l jmeter/results/test1.jtl",
    0.75, 6.55, 12.0, 0.3, size=12, color=LBLUE)

# ───────────────────────────────────────────────
# SLIDE 5 — GRAFANA (hyppo)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "hyppo")

txt(s, "Grafana — Visualisation Temps Réel", 0.5, 0.55, 11, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "À ouvrir PENDANT que JMeter tourne — on voit les courbes monter en direct",
    0.7, 1.25, 12, 0.4, size=16, color=GREY)

# URL
box(s, 0.5, 1.8, 12.3, 0.55, RGBColor(0x1A,0x1A,0x3E))
txt(s, "🌐  http://localhost:3000", 0.75, 1.88, 6.0, 0.38, size=15, bold=True, color=WHITE)
txt(s, "admin / admin   →  Dashboards  →  Gaming API - Performance Dashboard",
    0.75, 1.88, 12.0, 0.38, size=13, color=GREY)

# Métriques à surveiller
metrics = [
    ("⏱️",  "Latence p95 / p99",    "Temps de réponse des\nendpoints sous charge",      GREEN),
    ("🚀",  "Throughput",            "Nombre de requêtes\npar seconde",                   BLUE),
    ("💻",  "CPU & Mémoire JVM",     "Ressources consommées\npar l'application",          PURPLE),
    ("🔌",  "HikariCP",              "Connexions BDD utilisées\n(monte vers 20 max)",     ORANGE),
]
for i, (icon, title, desc, col) in enumerate(metrics):
    l = 0.5 + i * 3.15
    box(s, l, 2.6, 2.95, 2.6, col)
    txt(s, icon,  l, 2.68, 2.95, 0.85, size=40, align=PP_ALIGN.CENTER)
    txt(s, title, l, 3.53, 2.95, 0.55, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, desc,  l, 4.08, 2.95, 0.65, size=13, color=WHITE, align=PP_ALIGN.CENTER)

# Réglages importants
box(s, 0.5, 5.38, 12.3, 1.35, RGBColor(0x1A,0x1A,0x3E))
txt(s, "⚙️  Réglages indispensables :", 0.75, 5.46, 5.0, 0.38, size=14, bold=True, color=ORANGE)
settings = [
    ("📅  Période", "Last 15 minutes", BLUE),
    ("🔄  Refresh", "5s (icône horloge)", GREEN),
    ("📊  Avant/Après", "Last 30 min pour voir les 2 tests côte à côte", PURPLE),
]
for i, (label, val, col) in enumerate(settings):
    lx = 0.7 + i * 4.1
    txt(s, label, lx, 5.92, 2.0, 0.35, size=12, bold=True, color=col)
    txt(s, val,   lx, 6.28, 4.0, 0.35, size=12, color=GREY)

# ───────────────────────────────────────────────
# SLIDE 6 — PROMETHEUS / MICROMETER (Dilou)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Dilou")

txt(s, "Prometheus & Micrometer", 0.5, 0.55, 11, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "Prometheus collecte les métriques — Micrometer les expose depuis le code Java",
    0.7, 1.25, 12, 0.4, size=16, color=GREY)

# 3 cibles
box(s, 0.5, 1.78, 12.3, 0.45, RGBColor(0x1A,0x1A,0x3E))
txt(s, "3 cibles surveillées :", 0.75, 1.85, 3.5, 0.32, size=13, bold=True, color=ORANGE)
targets = [("prometheus :9090", GREY), ("gaming-api :8081", BLUE), ("gaming-gateway :8080", ORANGE)]
for i, (label, col) in enumerate(targets):
    pill(s, "● " + label, 4.1 + i * 2.8, 1.84, col)

# Métriques custom
box(s, 0.5, 2.38, 5.9, 3.25, RGBColor(0x1A,0x1A,0x3E))
txt(s, "📊  Métriques custom (métier)", 0.7, 2.46, 5.5, 0.42, size=14, bold=True, color=ORANGE)
custom = [
    ("dashboard_build_time",         "Temps de construction du dashboard"),
    ("match_created_total",          "Nombre de matchs créés"),
    ("player_stats_computation",     "Temps de calcul des stats joueur"),
    ("kafka_match_events_consumed",  "Events Kafka consommés"),
]
for i, (metric, desc) in enumerate(custom):
    y = 3.0 + i * 0.56
    box(s, 0.65, y, 5.6, 0.48, RGBColor(0x0D,0x0D,0x2A))
    txt(s, metric, 0.8,  y+0.06, 3.3, 0.35, size=11, bold=True, color=LBLUE)
    txt(s, desc,   4.15, y+0.06, 2.0, 0.35, size=11, color=GREY)

# PromQL
box(s, 6.6, 2.38, 6.2, 3.25, RGBColor(0x1A,0x1A,0x3E))
txt(s, "📈  Requêtes PromQL à coller", 6.8, 2.46, 5.8, 0.42, size=14, bold=True, color=ORANGE)
queries = [
    ("Débit req/s",  "rate(http_server_requests_seconds_count[1m])"),
    ("Latence p95",  "histogram_quantile(0.95, sum(rate(\nhttp_server_requests_seconds_bucket[1m]))\nby (le, uri))"),
    ("Matchs/s",     "rate(match_created_total[1m])"),
]
y = 3.0
for label, q in queries:
    txt(s, label, 6.75, y,      3.0, 0.32, size=12, bold=True, color=YELLOW)
    txt(s, q,     6.75, y+0.32, 6.0, 0.45, size=10, color=LBLUE)
    y += 0.9

# URL Prometheus
box(s, 0.5, 5.82, 12.3, 0.6, RGBColor(0x0D,0x1A,0x0D))
txt(s, "🌐  http://localhost:9090/targets  →  vérifier que les 3 cibles sont UP",
    0.75, 5.95, 12.0, 0.38, size=13, bold=True, color=GREEN)

# ───────────────────────────────────────────────
# SLIDE 7 — KAFKA (Nassim)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Nassim")

txt(s, "Kafka — Messaging Asynchrone", 0.5, 0.55, 11, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "L'API répond immédiatement — le traitement se fait en arrière-plan",
    0.7, 1.25, 12, 0.4, size=16, color=GREY)

# Flux
box(s, 0.5,  1.8, 3.0, 2.2, BLUE)
txt(s, "🎮",          0.5,  1.88, 3.0, 0.9,  size=40, align=PP_ALIGN.CENTER)
txt(s, "API",         0.5,  2.78, 3.0, 0.5,  size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "POST /api/matches\n→ répond 200 immédiat", 0.5, 3.3, 3.0, 0.55, size=12, color=GREY, align=PP_ALIGN.CENTER)

txt(s, "publier →\nmatch-events", 3.58, 2.55, 1.7, 0.7, size=12, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

box(s, 5.35, 1.8, 3.0, 2.2, RED)
txt(s, "📨",          5.35, 1.88, 3.0, 0.9,  size=40, align=PP_ALIGN.CENTER)
txt(s, "KAFKA",       5.35, 2.78, 3.0, 0.5,  size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "Topic : match-events\nMessage conservé", 5.35, 3.3, 3.0, 0.55, size=12, color=GREY, align=PP_ALIGN.CENTER)

txt(s, "consume →\nasync", 8.4, 2.55, 1.3, 0.7, size=12, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

box(s, 9.75, 1.8, 3.0, 2.2, GREEN)
txt(s, "⚙️",          9.75, 1.88, 3.0, 0.9,  size=40, align=PP_ALIGN.CENTER)
txt(s, "CONSUMER",    9.75, 2.78, 3.0, 0.5,  size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "Log + compteur\nPrometheus", 9.75, 3.3, 3.0, 0.55, size=12, color=GREY, align=PP_ALIGN.CENTER)

# Message JSON
box(s, 0.5, 4.2, 12.3, 0.65, RGBColor(0x0D,0x1A,0x2E))
txt(s, "Message publié :", 0.75, 4.28, 3.0, 0.35, size=13, bold=True, color=ORANGE)
txt(s, '{"event":"MATCH_CREATED","matchId":42,"gameMode":"RANKED","region":"EU"}',
    0.75, 4.28, 12.0, 0.35, size=13, color=LBLUE)

# Kafka UI
box(s, 0.5, 5.05, 5.8, 1.65, RGBColor(0x1A,0x1A,0x3E))
txt(s, "🌐  Kafka UI", 0.75, 5.13, 5.3, 0.4, size=14, bold=True, color=ORANGE)
txt(s, "http://localhost:8090", 0.75, 5.55, 5.3, 0.35, size=13, color=LBLUE)
txt(s, "Topics → match-events → Messages", 0.75, 5.93, 5.3, 0.35, size=12, color=GREY)
txt(s, "Consumers → gaming-group", 0.75, 6.3, 5.3, 0.35, size=12, color=GREY)

# Bénéfices
benefits = [("⚡", "Réponse\nimmédiate", "API ne bloque pas"), ("📈", "Scalable", "N consumers en parallèle"), ("📋", "Traçable", "Tous les events conservés")]
for i, (icon, title, desc) in enumerate(benefits):
    l = 6.6 + i * 2.25
    box(s, l, 5.05, 2.1, 1.65, RGBColor(0x1A,0x1A,0x3E))
    txt(s, icon,  l, 5.12, 2.1, 0.62, size=26, align=PP_ALIGN.CENTER)
    txt(s, title, l, 5.75, 2.1, 0.42, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, desc,  l, 6.18, 2.1, 0.42, size=11, color=GREY, align=PP_ALIGN.CENTER)

# ───────────────────────────────────────────────
# SLIDE 8 — AVANT / APRÈS
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Tous")

txt(s, "Avant / Après — Résultats Mesurés", 0.5, 0.55, 11, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)

# Colonnes
box(s, 0.5,  1.3, 5.85, 0.5, RED)
box(s, 7.0,  1.3, 5.85, 0.5, GREEN)
txt(s, "❌  AVANT  (branche demo-before)", 0.5,  1.38, 5.85, 0.36, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "✅  APRÈS  (branche gateway)",     7.0,  1.38, 5.85, 0.36, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "VS", 6.05, 1.38, 0.85, 0.36, size=18, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

rows = [
    ("GET /api/matches",       "⏳  Timeout — OOM (200k lignes RAM)",    "⚡  ~200ms (pagination SQL)"),
    ("GET /api/players/{id}",  "💥  Erreur 500 — cascade EAGER",         "✓   ~250ms  /  6ms (cache)"),
    ("GET /api/dashboard",     "🐢  2s+ — recalcul à chaque appel",      "🚀  ~450ms  /  6ms (cache)"),
    ("200 users simultanés",   "🔴  Saturé — pas de réponse",            "🟢  Stable — HikariCP pool=20"),
    ("Mémoire JVM",            "📈  OutOfMemory — crash",                 "📉  Stable — LAZY loading"),
]
y = 2.0
for label, before, after in rows:
    box(s, 0.5,  y, 5.85, 0.7, RGBColor(0x2A,0x10,0x10))
    box(s, 7.0,  y, 5.85, 0.7, RGBColor(0x0A,0x2A,0x15))
    txt(s, label,  0.5,  y+0.06, 5.85, 0.34, size=12, bold=True, color=GREY,  align=PP_ALIGN.CENTER)
    txt(s, before, 0.5,  y+0.38, 5.85, 0.3,  size=13, color=RED,              align=PP_ALIGN.CENTER)
    txt(s, after,  7.0,  y+0.18, 5.85, 0.45, size=13, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    txt(s, "→",    6.15, y+0.18, 0.7,  0.42, size=20, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    y += 0.79

box(s, 0.5, 6.0, 12.3, 0.75, RGBColor(0x1A,0x1A,0x3E))
txt(s, "🔬  Sur Grafana :", 0.75, 6.08, 2.5, 0.35, size=13, bold=True, color=ORANGE)
txt(s, "Mettre la période sur Last 30 min pendant la démo → les 2 tests JMeter apparaissent côte à côte",
    3.3, 6.08, 9.3, 0.35, size=13, color=WHITE)
txt(s, "Branche demo-before = cache désactivé  |  Branche gateway = toutes les optimisations actives",
    0.75, 6.46, 12.0, 0.28, size=11, color=GREY)

# ───────────────────────────────────────────────
# SLIDE 9 — CONCLUSION
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s)
box(s, 0, 0, 13.33, 0.5, ORANGE)
box(s, 0, 7.0, 13.33, 0.5, ORANGE)
speaker(s, "Tous")

txt(s, "Ce qu'on retient", 0, 0.65, 13.33, 0.75, size=34, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

lessons = [
    ("📏", "Mesurer avant d'optimiser",    "Sans métriques Prometheus/Grafana on navigue à l'aveugle"),
    ("🔍", "Chaque anti-pattern a un coût","EAGER loading, findAll(), pas de cache = crash en production"),
    ("🔀", "Architecturer pour la charge", "Gateway + pool HikariCP + cache = stabilité sous 200 users"),
    ("📨", "L'async libère l'API",         "Kafka découple les traitements lourds de la réponse HTTP"),
]
y = 1.6
for icon, title, desc in lessons:
    box(s, 0.5, y, 12.3, 1.05, BLUE)
    txt(s, icon,  0.6,  y+0.1,  1.1,  0.85, size=32, align=PP_ALIGN.CENTER)
    txt(s, title, 1.85, y+0.1,  5.5,  0.42, size=17, bold=True, color=WHITE)
    txt(s, desc,  1.85, y+0.52, 10.8, 0.42, size=14, color=GREY)
    y += 1.2

box(s, 0.5, 6.22, 12.3, 0.58, ORANGE)
txt(s, "\"Optimiser sans mesurer, c'est naviguer sans boussole.\"",
    0.5, 6.3, 12.3, 0.45, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

prs.save("/output/gaming_api_v4.pptx")
print("PPTX genere : gaming_api_v4.pptx")

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

DARK    = RGBColor(0x12, 0x12, 0x2B)
BLUE    = RGBColor(0x1A, 0x4F, 0x8A)
ORANGE  = RGBColor(0xF0, 0x6A, 0x1A)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
GREY    = RGBColor(0xCC, 0xCC, 0xCC)
GREEN   = RGBColor(0x2E, 0xCC, 0x71)
RED     = RGBColor(0xE7, 0x4C, 0x3C)
YELLOW  = RGBColor(0xF1, 0xC4, 0x0F)
LBLUE   = RGBColor(0x1A, 0x8C, 0xD8)

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

def speaker(slide, who):
    box(slide, 11.8, 0.08, 1.4, 0.3, ORANGE)
    txt(slide, who, 11.82, 0.09, 1.36, 0.28, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ───────────────────────────────────────────────
# SLIDE 1 — TITRE
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s)
box(s, 0, 0, 13.33, 7.5, DARK)
box(s, 0, 3.05, 13.33, 0.12, ORANGE)

txt(s, "🎮", 0, 0.7, 13.33, 1.2, size=72, align=PP_ALIGN.CENTER)
txt(s, "OPTIMISATION DES PERFORMANCES", 0, 1.9, 13.33, 0.8,
    size=30, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
txt(s, "d'une API Gaming en ligne", 0, 2.7, 13.33, 0.6,
    size=24, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "Spring Boot  ·  PostgreSQL  ·  Kafka  ·  Prometheus  ·  Grafana", 0, 3.4, 13.33, 0.5,
    size=15, color=GREY, align=PP_ALIGN.CENTER)
txt(s, "Groupe — 2026", 0, 6.8, 13.33, 0.4,
    size=13, color=GREY, align=PP_ALIGN.CENTER)

# ───────────────────────────────────────────────
# SLIDE 2 — LE PROJET  (P1)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Personne 1")

txt(s, "Le Projet", 0.5, 0.55, 12, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)

cards = [
    ("🎮", "Plateforme\nde jeu en ligne", "Matchs compétitifs\nentre joueurs",             BLUE,  0.5),
    ("👥", "10 000\nJoueurs",             "Répartis sur 4 régions\nmondiales",             BLUE,  4.6),
    ("🏆", "200 000\nParties",            "Avec scores,\nrésultats, durées",               BLUE,  8.7),
]
for icon, title, sub, col, l in cards:
    box(s, l, 1.5, 3.8, 4.5, col)
    txt(s, icon,  l,     1.65, 3.8, 1.2,  size=48, align=PP_ALIGN.CENTER)
    txt(s, title, l,     2.85, 3.8, 1.1,  size=22, bold=True, color=WHITE,   align=PP_ALIGN.CENTER)
    txt(s, sub,   l,     3.95, 3.8, 0.85, size=15, color=GREY,  align=PP_ALIGN.CENTER)

txt(s, "→  Une API REST qui doit répondre vite, même sous forte charge", 0.6, 6.3, 12.2, 0.55,
    size=17, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

# ───────────────────────────────────────────────
# SLIDE 3 — CE QU'ON A FAIT  (P1)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Personne 1")

txt(s, "Notre Démarche", 0.5, 0.55, 12, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)

steps = [
    ("1", "🏗️",  "CONSTRUIRE",  "L'API + la base de données\navec de vraies données", BLUE),
    ("2", "🔍",  "ANALYSER",    "Les problèmes de lenteur\ncachés dans le code",      RGBColor(0x8E, 0x44, 0xAD)),
    ("3", "📊",  "MESURER",     "Les performances\navant toute modification",         RGBColor(0xF3, 0x9C, 0x12)),
    ("4", "🚀",  "OPTIMISER",   "Corriger et mesurer\nà nouveau pour comparer",       GREEN),
]
for i, (num, icon, title, sub, col) in enumerate(steps):
    l = 0.5 + i * 3.15
    box(s, l, 1.5, 2.9, 4.5, col)
    txt(s, num,   l+0.1, 1.6,  2.7, 0.5,  size=14, bold=True, color=WHITE)
    txt(s, icon,  l,     2.1,  2.9, 1.1,  size=44, align=PP_ALIGN.CENTER)
    txt(s, title, l,     3.2,  2.9, 0.65, size=19, bold=True, color=WHITE,  align=PP_ALIGN.CENTER)
    txt(s, sub,   l,     3.9,  2.9, 0.9,  size=14, color=WHITE, align=PP_ALIGN.CENTER)
    if i < 3:
        txt(s, "→", l+2.93, 3.4, 0.4, 0.5, size=26, bold=True, color=ORANGE)

# ───────────────────────────────────────────────
# SLIDE 4 — LES PROBLÈMES  (P2)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Personne 2")

txt(s, "Les Problèmes Détectés", 0.5, 0.55, 12, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "L'API était lente — mais pourquoi ?", 0.7, 1.25, 12, 0.5, size=18, color=GREY)

problems = [
    ("💾", "SURCHARGE\nMÉMOIRE",  "L'API chargeait 200 000 parties\nd'un coup en mémoire",       RED,   0.5,  1.9),
    ("🔁", "TROP DE\nREQUÊTES",  "1 appel = des centaines de\nquestions à la base de données",  RED,   4.65, 1.9),
    ("⏳", "PAS DE\nCACHE",       "Les mêmes calculs refaits\nà chaque seconde",                  RED,   8.8,  1.9),
    ("🔍", "PAS\nD'INDEX",        "La base cherchait ligne par\nligne dans 200 000 entrées",      YELLOW, 0.5,  4.5),
    ("📦", "SAUVEGARDES\nUNITAIRES","Chaque joueur sauvegardé\nséparément, pas en groupe",       YELLOW, 4.65, 4.5),
    ("📉", "STATS\nEN JAVA",      "Calculs faits en code\nau lieu d'être faits par la BDD",      YELLOW, 8.8,  4.5),
]
for icon, title, desc, col, l, t in problems:
    box(s, l, t, 3.8, 2.3, col)
    txt(s, icon,  l,     t+0.1, 3.8, 0.85, size=36, align=PP_ALIGN.CENTER)
    txt(s, title, l,     t+0.95, 3.8, 0.7, size=17, bold=True, color=DARK,  align=PP_ALIGN.CENTER)
    txt(s, desc,  l,     t+1.65, 3.8, 0.6, size=12, color=DARK, align=PP_ALIGN.CENTER)

# ───────────────────────────────────────────────
# SLIDE 5 — L'OBSERVABILITÉ  (P3)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Personne 4")

txt(s, "Comment On Mesure Tout Ça ?", 0.5, 0.55, 12, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "Comme le tableau de bord d'une voiture — mais pour un serveur", 0.7, 1.25, 12, 0.45, size=17, color=GREY)

tools = [
    ("⚙️",  "MICROMETER",  "Capteurs intégrés\ndans l'application",   BLUE,                          0.5,  1.85),
    ("→",   "",            "",                                          DARK,                          4.45, 3.15),
    ("📡",  "PROMETHEUS",  "Collecte les données\ntoutes les 15 sec",  RGBColor(0x8E, 0x44, 0xAD),   4.65, 1.85),
    ("→",   "",            "",                                          DARK,                          8.6,  3.15),
    ("📊",  "GRAFANA",     "Affiche les courbes\nen temps réel",        GREEN,                         8.8,  1.85),
]
for icon, title, desc, col, l, t in tools:
    if title == "":
        txt(s, "→", l, t, 0.5, 0.6, size=30, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
        continue
    box(s, l, t, 3.8, 3.2, col)
    txt(s, icon,  l, t+0.1, 3.8, 1.1, size=44, align=PP_ALIGN.CENTER)
    txt(s, title, l, t+1.25, 3.8, 0.7, size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, desc,  l, t+2.0,  3.8, 0.85, size=14, color=WHITE, align=PP_ALIGN.CENTER)

box(s, 0.5, 5.3, 12.3, 1.35, RGBColor(0x1A, 0x1A, 0x3E))
txt(s, "Ce qu'on surveille :", 0.75, 5.42, 12, 0.4, size=14, bold=True, color=ORANGE)
txt(s, "⏱ Temps de réponse     💻 CPU du serveur     🧠 Mémoire utilisée     🧵 Nombre de processus actifs     🔌 Connexions à la base",
    0.75, 5.82, 12, 0.6, size=14, color=WHITE, align=PP_ALIGN.LEFT)

# ───────────────────────────────────────────────
# SLIDE 6 — KAFKA  (P4)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Personne 4")

txt(s, "Kafka — Événements en Temps Réel", 0.5, 0.55, 12, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)
txt(s, "Chaque action importante génère un événement traité en arrière-plan", 0.7, 1.25, 12, 0.45, size=17, color=GREY)

# Schéma flux Kafka
box(s, 0.5,  1.85, 3.5, 2.8, BLUE)
txt(s, "🎮",          0.5,  1.95, 3.5, 1.0, size=44, align=PP_ALIGN.CENTER)
txt(s, "API",         0.5,  2.95, 3.5, 0.55, size=20, bold=True, color=WHITE,  align=PP_ALIGN.CENTER)
txt(s, "Crée un match\net publie l'événement", 0.5, 3.5, 3.5, 0.7, size=13, color=GREY, align=PP_ALIGN.CENTER)

txt(s, "→\nmatch-events", 4.1, 2.5, 1.9, 1.0, size=15, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

box(s, 6.1,  1.85, 3.5, 2.8, RGBColor(0x8E, 0x44, 0xAD))
txt(s, "📨",          6.1,  1.95, 3.5, 1.0, size=44, align=PP_ALIGN.CENTER)
txt(s, "KAFKA",       6.1,  2.95, 3.5, 0.55, size=20, bold=True, color=WHITE,  align=PP_ALIGN.CENTER)
txt(s, "Topic : match-events\nStocke & distribue", 6.1, 3.5, 3.5, 0.7, size=13, color=GREY, align=PP_ALIGN.CENTER)

txt(s, "→\nconsume", 9.7, 2.5, 1.0, 1.0, size=15, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

box(s, 10.8, 1.85, 2.0, 2.8, GREEN)
txt(s, "⚙️",          10.8, 1.95, 2.0, 1.0, size=44, align=PP_ALIGN.CENTER)
txt(s, "CONSUMER",    10.8, 2.95, 2.0, 0.55, size=14, bold=True, color=WHITE,  align=PP_ALIGN.CENTER)
txt(s, "Traite\nasync", 10.8, 3.5, 2.0, 0.7, size=13, color=GREY, align=PP_ALIGN.CENTER)

# Message JSON exemple
box(s, 0.5, 4.9, 12.3, 1.0, RGBColor(0x0D, 0x1A, 0x2E))
txt(s, 'Message publié :', 0.75, 4.98, 4.0, 0.35, size=13, bold=True, color=ORANGE)
txt(s, '{"event":"MATCH_CREATED","matchId":42,"gameMode":"RANKED","region":"EU"}',
    0.75, 5.33, 11.8, 0.45, size=13, color=LBLUE)

# Bénéfices
benefits = [
    ("⚡", "Réponse\nimmédiate",   "L'API ne bloque pas\npour traiter l'event"),
    ("🔀", "Traitement\nparallèle","Plusieurs consumers\nen même temps"),
    ("📋", "Traçabilité\ncomplète","Tous les événements\nsont conservés"),
]
for i, (icon, title, desc) in enumerate(benefits):
    l = 0.5 + i * 4.2
    box(s, l, 6.1, 3.9, 1.1, RGBColor(0x1A, 0x1A, 0x3E))
    txt(s, icon,  l,      6.18, 1.1, 0.9, size=26, align=PP_ALIGN.CENTER)
    txt(s, title, l+1.15, 6.18, 2.6, 0.45, size=14, bold=True, color=WHITE)
    txt(s, desc,  l+1.15, 6.63, 2.6, 0.45, size=12, color=GREY)

# ───────────────────────────────────────────────
# SLIDE 7 — AVANT / APRÈS  (P5)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s); stripe(s); speaker(s, "Personne 3")

txt(s, "Avant et Après les Optimisations", 0.5, 0.55, 12, 0.6, size=32, bold=True, color=WHITE)
box(s, 0.5, 0.05, 0.08, 7.4, ORANGE)

box(s, 0.5,  1.3, 5.9, 0.55, RED)
box(s, 6.93, 1.3, 5.9, 0.55, GREEN)
txt(s, "❌  AVANT", 0.5,  1.38, 5.9, 0.4, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "✅  APRÈS", 6.93, 1.38, 5.9, 0.4, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "VS", 6.0, 1.38, 0.9, 0.4, size=20, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

rows = [
    ("Consulter les parties",  "⏳  Timeout (pas de réponse)", "⚡  Moins de 50ms"),
    ("Voir les meilleurs joueurs", "💥  Erreur 500 — plantage",   "✓  Réponse en 80ms"),
    ("Tableau de bord",        "🐢  2 secondes par requête",    "🚀  20ms (cache)"),
    ("200 utilisateurs en même temps", "🔴  Saturé, plus de réponse", "🟢  Stable, fluide"),
    ("Mémoire utilisée",       "📈  Explosion — OutOfMemory",   "📉  Stable et maîtrisée"),
]
y = 2.05
for label, before, after in rows:
    box(s, 0.5,  y, 5.9, 0.72, RGBColor(0x2A, 0x10, 0x10))
    box(s, 6.93, y, 5.9, 0.72, RGBColor(0x0A, 0x2A, 0x15))
    txt(s, label,  0.5,  y+0.12, 5.9, 0.5, size=13, bold=True, color=GREY,  align=PP_ALIGN.CENTER)
    txt(s, before, 0.5,  y+0.38, 5.9, 0.38, size=14, color=RED,   align=PP_ALIGN.CENTER)
    txt(s, after,  6.93, y+0.18, 5.9, 0.48, size=14, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    txt(s, "→", 6.1, y+0.18, 0.7, 0.45, size=20, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    y += 0.82

# ───────────────────────────────────────────────
# SLIDE 8 — CONCLUSION  (P5)
# ───────────────────────────────────────────────
s = prs.slides.add_slide(BLANK)
bg(s)
box(s, 0, 0, 13.33, 7.5, DARK)
box(s, 0, 0, 13.33, 0.5, ORANGE)
box(s, 0, 7.0, 13.33, 0.5, ORANGE)
speaker(s, "Personne 5")

txt(s, "Ce qu'on retient", 0, 0.65, 13.33, 0.75, size=34, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

lessons = [
    ("📏", "Mesurer d'abord",         "On ne peut pas améliorer ce qu'on ne mesure pas"),
    ("🔍", "Comprendre avant d'agir", "Chaque lenteur a une cause identifiable"),
    ("📊", "L'observabilité, c'est vital", "Sans tableau de bord, on navigue à l'aveugle"),
    ("🏆", "Les petits détails comptent", "Un seul mauvais paramètre peut tout bloquer"),
]
y = 1.55
for icon, title, desc in lessons:
    box(s, 0.5, y, 12.3, 1.1, BLUE)
    txt(s, icon,  0.55, y+0.1, 1.1, 0.9,  size=32, align=PP_ALIGN.CENTER)
    txt(s, title, 1.75, y+0.1, 5.0, 0.45, size=18, bold=True, color=WHITE)
    txt(s, desc,  1.75, y+0.55, 10.8, 0.45, size=15, color=GREY)
    y += 1.25

box(s, 0.5, 6.3, 12.3, 0.6, ORANGE)
txt(s, "\"Optimiser sans mesurer, c'est naviguer sans boussole.\"",
    0.5, 6.36, 12.3, 0.48, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

prs.save("/output/gaming_api_v3.pptx")
print("✅  PPTX généré !")

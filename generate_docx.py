from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Marges ──────────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)

# ── Helpers ──────────────────────────────────────────────────────────────────
def heading(text, level=1, color=(0xF0, 0x6A, 0x1A)):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in p.runs:
        run.font.color.rgb = RGBColor(*color)
    return p

def para(text, bold=False, italic=False, size=11, color=(0x20, 0x20, 0x20), indent=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(text)
    run.bold   = bold
    run.italic = italic
    run.font.size  = Pt(size)
    run.font.color.rgb = RGBColor(*color)
    return p

def quote(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(1.2)
    p.paragraph_format.right_indent = Cm(1.2)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.italic = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x30, 0x30, 0x30)
    # bordure gauche bleue
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '18')
    left.set(qn('w:space'), '10')
    left.set(qn('w:color'), 'F06A1A')
    pBdr.append(left)
    pPr.append(pBdr)
    return p

def separator():
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single')
    bot.set(qn('w:sz'), '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), 'CCCCCC')
    pBdr.append(bot)
    pPr.append(pBdr)

def speaker_tag(name, slides):
    p = doc.add_paragraph()
    run1 = p.add_run(f"  {name}  ")
    run1.bold = True
    run1.font.size = Pt(12)
    run1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    # fond orange simulé via highlight (pas natif en docx, on utilise shading)
    rPr = run1._r.get_or_add_rPr()
    highlight = OxmlElement('w:highlight')
    highlight.set(qn('w:val'), 'darkYellow')
    rPr.append(highlight)
    run2 = p.add_run(f"   {slides}")
    run2.font.size  = Pt(11)
    run2.italic = True
    run2.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)

# ── PAGE DE TITRE ────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("🎮  SCRIPT DE PRÉSENTATION ORAL")
run.bold = True
run.font.size = Pt(20)
run.font.color.rgb = RGBColor(0xF0, 0x6A, 0x1A)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("Optimisation des Performances Backend Java — API Gaming")
r2.font.size = Pt(14)
r2.font.color.rgb = RGBColor(0x1A, 0x4F, 0x8A)
r2.bold = True

p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r3 = p3.add_run("Groupe de 5 personnes  ·  2026  ·  ~4 minutes par personne")
r3.font.size = Pt(11)
r3.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
r3.italic = True

doc.add_paragraph()
separator()
doc.add_paragraph()

# ── GUIDE RAPIDE ─────────────────────────────────────────────────────────────
heading("Guide de lecture", level=2, color=(0x1A, 0x4F, 0x8A))
para("• Le texte en italique entre guillemets = ce que vous dites à l'oral", size=10)
para("• Adaptez avec vos propres mots — ce script est un guide, pas une récitation", size=10)
para("• Durée cible : 3 à 4 minutes par personne", size=10)
doc.add_paragraph()
separator()

# ══════════════════════════════════════════════════════════════════════════════
# PERSONNE 1
# ══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
heading("PERSONNE 1", level=1)
speaker_tag("Personne 1", "Slides 1, 2, 3  —  Introduction, Le Projet, Notre Démarche")
doc.add_paragraph()

heading("Slide 1 — Titre", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Bonjour à tous. Aujourd'hui on va vous présenter notre projet : l'optimisation des performances d'une API gaming.")
doc.add_paragraph()
quote("Pour ceux qui ne sont pas techniques, pas d'inquiétude — on va tout expliquer simplement. L'idée de base, c'est qu'on a construit un serveur pour un jeu vidéo en ligne, et on a cherché à comprendre pourquoi il était lent... et comment le rendre rapide.")
doc.add_paragraph()

heading("Slide 2 — Le Projet", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Concrètement, qu'est-ce qu'on a construit ?")
doc.add_paragraph()
quote("Imaginez une plateforme de jeu compétitif en ligne — comme un service qui gère les matchs entre joueurs. Notre API, c'est le moteur derrière tout ça.")
doc.add_paragraph()
quote("On a 10 000 joueurs enregistrés, répartis dans le monde entier. 200 000 parties jouées. Et pour chaque partie, on stocke les scores, les résultats, les durées... ça fait environ 700 000 entrées en base de données.")
doc.add_paragraph()
quote("L'enjeu, c'est que quand des milliers de joueurs se connectent en même temps, le serveur doit répondre vite. Et au départ, ce n'était pas le cas.")
doc.add_paragraph()

heading("Slide 3 — Notre Démarche", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Pour résoudre ça, on a suivi une méthode en 4 étapes.")
doc.add_paragraph()
quote("D'abord on a CONSTRUIT l'application complète avec toutes les données de test.")
doc.add_paragraph()
quote("Ensuite on a ANALYSÉ le code pour trouver les mauvaises pratiques — on appelle ça des anti-patterns, des façons de coder qui marchent mais qui ralentissent tout.")
doc.add_paragraph()
quote("Puis on a MESURÉ les performances réelles — les temps de réponse, la mémoire utilisée, le nombre de requêtes... avant de toucher quoi que ce soit.")
doc.add_paragraph()
quote("Et enfin on a OPTIMISÉ, corrigé les problèmes, et mesuré à nouveau pour prouver que ça allait mieux.")
doc.add_paragraph()
quote("C'est comme un médecin qui fait un bilan de santé avant de prescrire un traitement.")

separator()

# ══════════════════════════════════════════════════════════════════════════════
# PERSONNE 2
# ══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
heading("PERSONNE 2", level=1)
speaker_tag("Personne 2", "Slide 4  —  Les Problèmes Détectés")
doc.add_paragraph()

heading("Slide 4 — Les Problèmes Détectés", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Alors, qu'est-ce qu'on a trouvé comme problèmes ?")
doc.add_paragraph()
quote("On en a identifié six. Je vais vous les expliquer simplement.")
doc.add_paragraph()
quote("Le premier, c'est la SURCHARGE MÉMOIRE. Imaginez que pour vous montrer 5 parties, le serveur charge les 200 000 parties en mémoire d'un coup — comme si pour vous donner une cuillère de soupe, on vous apportait toute la casserole. Résultat : le serveur s'effondre.")
doc.add_paragraph()
quote("Le deuxième, c'est TROP DE REQUÊTES. Pour répondre à une seule question, le serveur posait des centaines de questions à la base de données. Un peu comme si pour vous dire l'heure, on appelait 300 personnes différentes.")
doc.add_paragraph()
quote("Le troisième : PAS DE CACHE. Les mêmes calculs lourds étaient refaits à chaque seconde, même si rien n'avait changé. Comme si vous recalculiez 2+2 à chaque fois au lieu de mémoriser que ça fait 4.")
doc.add_paragraph()
quote("Les trois autres — pas d'index, sauvegardes unitaires, calculs mal placés — c'est le même principe : des raccourcis qui n'ont pas été pris, et qui coûtaient cher en performance.")
doc.add_paragraph()
quote("Résultat concret : l'API était pratiquement inutilisable sous charge.")

separator()

# ══════════════════════════════════════════════════════════════════════════════
# PERSONNE 3
# ══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
heading("PERSONNE 3", level=1)
speaker_tag("Personne 3", "Slide 5  —  Comment on mesure tout ça")
doc.add_paragraph()

heading("Slide 5 — Comment on mesure tout ça ?", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Maintenant, comment est-ce qu'on a détecté et suivi ces problèmes ?")
doc.add_paragraph()
quote("On a mis en place ce qu'on appelle une stack d'observabilité. C'est un peu comme le tableau de bord d'une voiture — ça vous dit en temps réel si le moteur chauffe, si vous avez assez d'essence, si quelque chose ne va pas.")
doc.add_paragraph()
quote("On a trois outils qui travaillent ensemble.")
doc.add_paragraph()
quote("MICROMETER, c'est les capteurs — il est intégré directement dans l'application et mesure tout en continu : combien de temps met chaque requête, combien de mémoire est utilisée, combien de processus tournent en parallèle...")
doc.add_paragraph()
quote("PROMETHEUS, c'est l'enregistreur — il vient collecter ces données toutes les 15 secondes et les stocke dans le temps.")
doc.add_paragraph()
quote("Et GRAFANA, c'est l'écran — il affiche toutes ces données sous forme de graphiques, en direct, pendant qu'on fait tourner les tests.")
doc.add_paragraph()
quote("Ce qu'on surveille concrètement : le temps de réponse de chaque endpoint, le CPU du serveur, la mémoire utilisée, le nombre de connexions actives à la base de données, et les pauses du garbage collector — c'est le mécanisme qui nettoie la mémoire Java.")
doc.add_paragraph()
quote("Grâce à ça, on voit exactement quand et pourquoi le serveur ralentit.")

separator()

# ══════════════════════════════════════════════════════════════════════════════
# PERSONNE 4
# ══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
heading("PERSONNE 4", level=1)
speaker_tag("Personne 4", "Slide 6  —  Tests de Charge JMeter")
doc.add_paragraph()

heading("Slide 6 — Simuler des Milliers d'Utilisateurs", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Pour stresser vraiment l'application, on a utilisé Apache JMeter. C'est un outil qui simule des dizaines ou des centaines d'utilisateurs en même temps.")
doc.add_paragraph()
quote("On a créé trois scénarios.")
doc.add_paragraph()
quote("Le premier : LECTURE MASSIVE. On simule 100 utilisateurs qui consultent des parties en même temps, pendant 3 minutes. C'est le cas typique d'un lundi matin où tout le monde se connecte.")
doc.add_paragraph()
quote("Le deuxième : ÉCRITURE CONCURRENTE. 50 utilisateurs qui créent des parties en même temps, pendant 2 minutes. C'est ce qui se passe pendant un tournoi.")
doc.add_paragraph()
quote("Le troisième : SCÉNARIO MIXTE. C'est le plus réaliste — 200 utilisateurs, dont 70% qui lisent et 30% qui créent des parties, pendant 5 minutes. C'est le comportement normal d'une vraie plateforme.")
doc.add_paragraph()
quote("Et pendant tous ces tests, Grafana affiche en direct ce qui se passe sur le serveur. On voit les courbes monter, on voit quand ça sature, on voit exactement où se situe le point de rupture.")

separator()

# ══════════════════════════════════════════════════════════════════════════════
# PERSONNE 5
# ══════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
heading("PERSONNE 5", level=1)
speaker_tag("Personne 5", "Slides 7, 8  —  Avant/Après et Conclusion")
doc.add_paragraph()

heading("Slide 7 — Avant et Après les Optimisations", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Maintenant, les résultats concrets.")
doc.add_paragraph()
quote("Avant les optimisations, le constat était sévère. Consulter une liste de parties ? Timeout — le serveur ne répondait pas. Voir le classement des meilleurs joueurs ? Erreur 500, crash. La mémoire explosait, les connexions saturaient.")
doc.add_paragraph()
quote("Après les corrections, la situation est radicalement différente.")
doc.add_paragraph()
quote("On est passés de \"pas de réponse\" à moins de 50 millisecondes. Du classement joueurs qui plantait à une réponse en 80ms. Du tableau de bord qui prenait 2 secondes à 20 millisecondes grâce au cache.")
doc.add_paragraph()
quote("Et sous 200 utilisateurs simultanés — ce qui était le scénario de la mort avant — le serveur reste stable et fluide.")
doc.add_paragraph()
quote("Ces améliorations ont été obtenues en corrigeant les six problèmes qu'on vous a montrés : le chargement à la demande des données, la pagination côté base de données, la mise en cache, les index, et le regroupement des sauvegardes.")
doc.add_paragraph()

heading("Slide 8 — Conclusion", level=2, color=(0x1A, 0x4F, 0x8A))
quote("Pour conclure, ce projet nous a appris quatre choses essentielles.")
doc.add_paragraph()
quote("Un : MESURER D'ABORD. On ne peut pas améliorer ce qu'on ne mesure pas. Sans Grafana et Prometheus, on aurait codé dans le vide.")
doc.add_paragraph()
quote("Deux : COMPRENDRE AVANT D'AGIR. Chaque lenteur avait une cause précise. Ce n'était pas \"le serveur est lent\", c'était \"cette ligne de code charge 200 000 lignes inutilement\".")
doc.add_paragraph()
quote("Trois : L'OBSERVABILITÉ N'EST PAS OPTIONNELLE. En production, sans tableau de bord, on navigue à l'aveugle. Les problèmes ne se voient pas dans le code, ils se voient dans les métriques.")
doc.add_paragraph()
quote("Quatre : LES PETITS DÉTAILS COMPTENT ÉNORMÉMENT. Un seul paramètre mal configuré peut rendre une application inutilisable à l'échelle.")
doc.add_paragraph()
quote("Comme on aime le dire : \"Optimiser sans mesurer, c'est naviguer sans boussole.\"")
doc.add_paragraph()
quote("Merci pour votre attention. On est disponibles pour vos questions.")

separator()

# ── Pied de page ─────────────────────────────────────────────────────────────
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Gaming Performance API  —  Script Oral  —  2026")
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
r.italic = True

doc.save("/output/script_oral_gaming_api.docx")
print("✅  Word généré !")

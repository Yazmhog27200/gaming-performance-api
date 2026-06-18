from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

for section in doc.sections:
    section.top_margin    = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)

# ── Helpers ───────────────────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = RGBColor(0xF0, 0x6A, 0x1A)
    return p

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(0x1A, 0x4F, 0x8A)
    return p

def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    return p

def body(text, indent=False, color=(0x22,0x22,0x22), size=11):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor(*color)
    return p

def speech(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(1.0)
    p.paragraph_format.right_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(3)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '18')
    left.set(qn('w:space'), '10')
    left.set(qn('w:color'), 'F06A1A')
    pBdr.append(left)
    pPr.append(pBdr)
    r = p.add_run(f'"{text}"')
    r.italic = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x33,0x33,0x33)

def cmd(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), '1E1E2E')
    pPr.append(shd)
    r = p.add_run(f'  {text}  ')
    r.font.name = 'Courier New'
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x00, 0xFF, 0x88)

def url(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(f'→  {text}')
    r.font.size = Pt(11)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1A, 0x4F, 0x8A)

def tip(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'FFF3CD')
    pPr.append(shd)
    r = p.add_run(f'  💡  {text}')
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x55, 0x44, 0x00)

def separator():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single')
    bot.set(qn('w:sz'), '6')
    bot.set(qn('w:space'), '1')
    bot.set(qn('w:color'), 'CCCCCC')
    pBdr.append(bot)
    pPr.append(pBdr)

def person_banner(name, slides, duration):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(6)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), '1A4F8A')
    pPr.append(shd)
    r = p.add_run(f'  {name}  —  {slides}  —  ⏱ {duration}  ')
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)

def step_label(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0xF0, 0x6A, 0x1A)

# ═════════════════════════════════════════════════════════════════════════════
#  PAGE DE TITRE
# ═════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('GUIDE DE PRÉSENTATION COMPLET')
r.bold = True; r.font.size = Pt(22)
r.font.color.rgb = RGBColor(0xF0, 0x6A, 0x1A)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Optimisation des Performances Backend Java — API Gaming')
r.bold = True; r.font.size = Pt(15)
r.font.color.rgb = RGBColor(0x1A, 0x4F, 0x8A)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Ce document contient : quoi montrer • quoi dire • quelles commandes taper • pourquoi ça sert')
r.italic = True; r.font.size = Pt(11)
r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

separator()
doc.add_paragraph()

# ── LÉGENDE ──────────────────────────────────────────────────────────────────
h2('📖  Comment lire ce document')
body('🗣  Texte en italique entre guillemets  =  ce que vous dites à l\'oral', indent=True)
body('⌨  Fond sombre vert  =  commande à taper dans le terminal PowerShell', indent=True)
body('🔗  Texte bleu en gras  =  URL à ouvrir dans le navigateur', indent=True)
body('💡  Fond jaune  =  conseil ou info importante', indent=True)
separator()

# ── AVANT DE COMMENCER ────────────────────────────────────────────────────────
h2('⚡  AVANT DE COMMENCER — À faire 5 minutes avant la présentation')
body('1.  Ouvrir un terminal PowerShell dans le dossier du projet :', indent=True)
cmd('cd C:\\Users\\Utilisateur\\gaming-performance-api')
body('2.  Lancer tous les services :', indent=True)
cmd('docker compose up -d')
body('3.  Attendre 30 secondes que tout démarre, puis vérifier :', indent=True)
cmd('docker compose ps')
tip('Tous les services doivent afficher "Up". Si ce n\'est pas le cas, attendez encore 20 secondes.')
body('4.  Ouvrir ces 3 onglets dans le navigateur :', indent=True)
url('http://localhost:8080/actuator/health        ← santé de l\'API')
url('http://localhost:9090                        ← Prometheus')
url('http://localhost:3000                        ← Grafana  (admin / admin)')
doc.add_paragraph()
separator()

# ═════════════════════════════════════════════════════════════════════════════
#  PERSONNE 1
# ═════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
h1('👤  PERSONNE 1')
person_banner('Personne 1', 'Slides 1 → 3', '3 à 4 minutes')

# --- Slide 1 ---
h2('SLIDE 1 — Titre')
step_label('Ce que vous faites :')
body('Restez sur le slide de titre, regardez l\'audience.', indent=True)
step_label('Ce que vous dites :')
speech('Bonjour à tous. Aujourd\'hui on va vous présenter notre projet : l\'optimisation des performances d\'une API gaming. Pour ceux qui ne sont pas techniques, pas d\'inquiétude — on va tout expliquer simplement. L\'idée de base : on a construit un serveur pour un jeu vidéo en ligne, et on a cherché pourquoi il était lent... et comment le rendre rapide.')

# --- Slide 2 ---
h2('SLIDE 2 — Le Projet')
step_label('Ce que vous faites :')
body('Passez sur le slide 2. Montrez les 3 cartes : 10 000 joueurs, 200 000 parties.', indent=True)
step_label('Ce que vous dites :')
speech('Concrètement, on a construit une plateforme de jeu compétitif en ligne. Notre API, c\'est le moteur derrière tout ça. On gère 10 000 joueurs répartis dans le monde entier, 200 000 parties jouées, et pour chaque partie : les scores, les résultats, les durées. Ça représente environ 700 000 entrées en base de données. L\'enjeu : quand des milliers de joueurs se connectent en même temps, le serveur doit répondre vite. Et au départ, ce n\'était pas du tout le cas.')

# --- Slide 3 ---
h2('SLIDE 3 — Notre Démarche')
step_label('Ce que vous faites :')
body('Passez sur le slide 3. Pointez chaque étape en parlant.', indent=True)
step_label('Ce que vous dites :')
speech('Pour résoudre ça, on a suivi une méthode en 4 étapes. D\'abord CONSTRUIRE — l\'application complète avec toutes les données. Ensuite ANALYSER — trouver les mauvaises pratiques cachées dans le code. Puis MESURER — les performances réelles, avant de toucher quoi que ce soit. Et enfin OPTIMISER — corriger et mesurer à nouveau pour prouver que ça allait mieux. C\'est comme un médecin qui fait un bilan de santé avant de prescrire un traitement.')
separator()

# ═════════════════════════════════════════════════════════════════════════════
#  PERSONNE 2
# ═════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
h1('👤  PERSONNE 2')
person_banner('Personne 2', 'Slide 4  +  Démo en direct des anti-patterns', '4 à 5 minutes')
tip('Cette partie est la plus technique mais aussi la plus impressionnante. Suivez les étapes dans l\'ordre.')

h2('SLIDE 4 — Les Problèmes Détectés')
step_label('Ce que vous dites d\'abord (sans rien taper) :')
speech('Alors, qu\'est-ce qu\'on a trouvé comme problèmes ? On en a identifié six. Je vais vous montrer les trois principaux en direct sur l\'écran.')

# ANTI-PATTERN 1
h3('─── DÉMO 1 : Le problème N+1 — "Trop de requêtes"')
step_label('Pourquoi ça existe (à comprendre) :')
body('Le code est configuré pour charger automatiquement TOUTES les données liées à chaque entité. Quand on charge 1 match, il charge aussi ses joueurs, et les matchs de ces joueurs, et les joueurs de ces matchs... C\'est une cascade infinie de requêtes SQL.', indent=True)
step_label('Ouvrez le code dans l\'IDE — montrez ce fichier :')
body('gaming-performance-api/src/main/java/com/gaming/api/entity/Match.java  ligne 53', indent=True)
body('Montrez cette ligne et expliquez :', indent=True)
cmd('fetch = FetchType.EAGER')
step_label('Ce que vous dites :')
speech('Ici on voit "EAGER" — ça veut dire que dès qu\'on touche un match, le code charge automatiquement TOUT ce qui est lié. C\'est comme si en voulant lire le titre d\'un livre, on téléchargeait toute la bibliothèque.')
step_label('Maintenant montrez-le en direct — ouvrez le terminal et tapez :')
cmd('docker logs gaming-api -f 2>&1 | Select-String "select"')
step_label('Dans un 2e onglet du navigateur, ouvrez :')
url('http://localhost:8080/api/matches/1')
step_label('Ce que vous dites en montrant les logs qui défilent :')
speech('Regardez le terminal — une seule requête de notre part déclenche des dizaines et des dizaines de requêtes SQL en cascade. C\'est le problème N+1 : 1 appel = N requêtes cachées.')
tip('Appuyez sur Ctrl+C pour arrêter les logs une fois que vous avez montré l\'effet.')

# ANTI-PATTERN 2
h3('─── DÉMO 2 : findAll() — "Surcharge mémoire"')
step_label('Pourquoi ça existe (à comprendre) :')
body('Au lieu de demander à la base de données de paginer les résultats, le code charge TOUTES les 200 000 lignes en mémoire d\'un coup, puis fait le tri en Java. C\'est comme vider un entrepôt pour trouver 1 boîte.', indent=True)
step_label('Montrez ce fichier dans l\'IDE :')
body('gaming-performance-api/src/main/java/com/gaming/api/service/MatchService.java  ligne 58', indent=True)
step_label('Ce que vous dites :')
speech('Regardez cette ligne : "findAll()". Ça charge les 200 000 parties en mémoire d\'un coup. Et là, "subList()" fait la pagination côté Java au lieu de laisser la base de données le faire. Résultat : le serveur s\'effondre.')
step_label('Pour montrer l\'impact, ouvrez Grafana :')
url('http://localhost:3000')
body('Allez dans le dashboard "Gaming Performance API" — montrez le panel Mémoire Heap.', indent=True)
step_label('Ce que vous dites :')
speech('Sur ce graphique, on voit la mémoire utilisée par le serveur. Dès qu\'on appelle cet endpoint, elle monte brutalement.')

# ANTI-PATTERN 3
h3('─── DÉMO 3 : Pas de cache — "Calculs répétés"')
step_label('Pourquoi ça existe (à comprendre) :')
body('Le tableau de bord de l\'API recalcule toutes ses statistiques à chaque fois qu\'on l\'appelle. Même si rien n\'a changé depuis la dernière seconde, tout est recalculé depuis zéro.', indent=True)
step_label('Ouvrez Prometheus et tapez cette requête :')
url('http://localhost:9090')
body('Dans la barre de recherche Prometheus, tapez :', indent=True)
cmd('http_server_requests_seconds_sum{uri="/api/dashboard"}')
body('Cliquez sur Execute puis sur l\'onglet Graph.', indent=True)
step_label('Ce que vous dites :')
speech('Chaque pic sur ce graphique représente un appel au tableau de bord. Vous voyez que le temps monte à chaque fois — parce qu\'il recalcule tout. Avec un cache, ce serait plat après le premier appel.')
separator()

# ═════════════════════════════════════════════════════════════════════════════
#  PERSONNE 3
# ═════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
h1('👤  PERSONNE 3')
person_banner('Personne 3', 'Slide 5  +  Démo Prometheus & Grafana', '4 à 5 minutes')

h2('SLIDE 5 — Comment on mesure tout ça ?')
step_label('Ce que vous dites pour introduire :')
speech('Maintenant, comment est-ce qu\'on voit et suit ces problèmes en temps réel ? On a mis en place une stack d\'observabilité — c\'est un ensemble d\'outils qui surveillent le serveur en permanence, comme le tableau de bord d\'une voiture.')
body('Expliquez les 3 outils du slide :', indent=True)
speech('MICROMETER, c\'est les capteurs — intégré dans l\'application, il mesure tout en continu. PROMETHEUS, c\'est l\'enregistreur — il collecte ces données toutes les 15 secondes. Et GRAFANA, c\'est l\'écran — il affiche tout sous forme de graphiques en direct.')

h2('DÉMO 1 — Prometheus : voir les métriques brutes')
step_label('Ouvrez Prometheus :')
url('http://localhost:9090')
step_label('Allez dans Status → Targets et montrez :')
body('Vous verrez "gaming-performance-api" avec le statut UP en vert. C\'est la preuve que Prometheus est bien connecté à l\'API et collecte ses données.', indent=True)
step_label('Ce que vous dites :')
speech('Ici on voit que Prometheus "scrape" notre API toutes les 15 secondes. Il est bien connecté et actif.')
step_label('Retournez sur la page principale et tapez ces requêtes une par une :')
cmd('jvm_memory_used_bytes')
body('→ Montre la mémoire utilisée par Java en ce moment.', indent=True)
cmd('http_server_requests_seconds_count')
body('→ Montre le nombre total de requêtes reçues par l\'API.', indent=True)
cmd('hikaricp_connections_active')
body('→ Montre combien de connexions à la base de données sont actives.', indent=True)
step_label('Ce que vous dites :')
speech('Toutes ces métriques sont collectées automatiquement par Micrometer, sans qu\'on ait eu à écrire de code spécifique. C\'est la puissance de l\'observabilité.')

h2('DÉMO 2 — Grafana : les graphiques en temps réel')
step_label('Ouvrez Grafana :')
url('http://localhost:3000')
body('Identifiants : admin / admin. Le dashboard s\'ouvre automatiquement.', indent=True)
step_label('Montrez chaque panel en expliquant :')
body('Panel "Temps de réponse HTTP (p50/p95/p99)" :', indent=True)
speech('Ces trois courbes montrent les temps de réponse. P50 = la moitié des requêtes sont plus rapides que ça. P95 = 95% des requêtes sont sous ce seuil. P99 = le pire cas pour 99% des requêtes. Plus les courbes sont hautes, plus l\'API est lente.')
body('Panel "Mémoire Heap" :', indent=True)
speech('La mémoire heap, c\'est l\'espace de travail de Java. Quand elle est pleine, le serveur plante. On voit ici qu\'avec les anti-patterns, elle monte rapidement.')
body('Panel "Pool JDBC — Connexions HikariCP" :', indent=True)
speech('Ce panel montre les connexions à la base de données. Quand toutes les connexions sont occupées, les nouvelles requêtes attendent — c\'est là que l\'API se bloque.')
tip('Si les graphiques sont vides, générez du trafic en ouvrant http://localhost:8080/actuator/health plusieurs fois, puis rafraîchissez Grafana.')
separator()

# ═════════════════════════════════════════════════════════════════════════════
#  PERSONNE 4
# ═════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
h1('👤  PERSONNE 4')
person_banner('Personne 4', 'Slide 6  +  Explication JMeter', '3 à 4 minutes')

h2('SLIDE 6 — Simuler des Milliers d\'Utilisateurs')
step_label('Ce que vous dites pour introduire :')
speech('Pour vraiment stresser l\'application et mesurer ses limites, on a utilisé Apache JMeter. C\'est un outil qui simule des centaines d\'utilisateurs qui se connectent en même temps.')
step_label('Expliquez les 3 scénarios du slide :')
body('Scénario 1 — Lecture massive :', indent=True)
speech('On simule 100 utilisateurs qui consultent des parties en même temps, pendant 3 minutes. C\'est ce qui se passe un lundi matin quand tout le monde se connecte après le week-end.')
body('Scénario 2 — Écriture concurrente :', indent=True)
speech('50 utilisateurs créent des parties en même temps, pendant 2 minutes. C\'est ce qui se passe pendant un tournoi — tout le monde démarre en même temps.')
body('Scénario 3 — Scénario mixte :', indent=True)
speech('200 utilisateurs, 70% lisent, 30% créent des parties, pendant 5 minutes. C\'est le scénario le plus réaliste — il représente l\'utilisation normale d\'une vraie plateforme gaming.')

h2('Comment on lit les résultats JMeter')
step_label('Les fichiers de test sont dans le projet :')
body('gaming-performance-api/jmeter/01-scenario-lecture-massive.jmx', indent=True)
body('gaming-performance-api/jmeter/02-scenario-ecriture-concurrente.jmx', indent=True)
body('gaming-performance-api/jmeter/03-scenario-mixte.jmx', indent=True)
step_label('Ce qu\'on analyse après chaque test :')
body('• Temps de réponse moyen  →  est-ce que l\'API répond vite ?', indent=True)
body('• Taux d\'erreur           →  combien de requêtes échouent ?', indent=True)
body('• Throughput              →  combien de requêtes par seconde peut-on gérer ?', indent=True)
body('• Pics sur Grafana        →  qu\'est-ce qui lâche en premier ?', indent=True)
step_label('Ce que vous dites pour conclure cette partie :')
speech('Ces tests nous permettent de savoir exactement à quel moment l\'application craque, et quelle partie est responsable. Sans ces mesures, on ne saurait pas quoi optimiser en priorité.')
separator()

# ═════════════════════════════════════════════════════════════════════════════
#  PERSONNE 5
# ═════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
h1('👤  PERSONNE 5')
person_banner('Personne 5', 'Slides 7 & 8  —  Avant/Après et Conclusion', '3 à 4 minutes')

h2('SLIDE 7 — Avant et Après les Optimisations')
step_label('Ce que vous dites :')
speech('Voici les résultats concrets. Avant les optimisations, le constat était sévère.')
body('Parcourez le tableau ligne par ligne :', indent=True)
speech('Consulter une liste de parties : timeout — le serveur ne répondait pas. Voir le classement des meilleurs joueurs : erreur 500, crash. La mémoire explosait, les connexions saturaient.')
speech('Après les corrections, tout change. On est passés de "pas de réponse" à moins de 50 millisecondes. Du plantage à une réponse en 80ms. Du tableau de bord à 2 secondes à 20 millisecondes grâce au cache.')
step_label('Expliquez les 5 optimisations appliquées :')
body('1.  Chargement à la demande  →  on ne charge plus les données inutilement', indent=True)
body('2.  Pagination en base de données  →  on ne charge plus 200 000 lignes d\'un coup', indent=True)
body('3.  Cache  →  les calculs déjà faits sont mémorisés pendant 10 à 60 secondes', indent=True)
body('4.  Index SQL  →  la base de données trouve les données en millisecondes au lieu de tout scanner', indent=True)
body('5.  Regroupement des sauvegardes  →  on insère tout en une seule opération au lieu de 1 par 1', indent=True)
speech('Ces améliorations ont été obtenues uniquement en corrigeant des erreurs de conception — sans changer le matériel, sans augmenter les serveurs.')

h2('SLIDE 8 — Conclusion')
step_label('Ce que vous dites :')
speech('Pour conclure, ce projet nous a appris quatre choses essentielles.')
speech('Un : MESURER D\'ABORD. On ne peut pas améliorer ce qu\'on ne mesure pas. Sans Grafana et Prometheus, on aurait codé dans le vide.')
speech('Deux : COMPRENDRE AVANT D\'AGIR. Chaque lenteur avait une cause précise. Ce n\'était pas "le serveur est lent", c\'était "cette ligne de code charge 200 000 lignes inutilement".')
speech('Trois : L\'OBSERVABILITÉ N\'EST PAS OPTIONNELLE. En production, sans tableau de bord, on navigue à l\'aveugle.')
speech('Quatre : LES PETITS DÉTAILS COMPTENT ÉNORMÉMENT. Un seul paramètre mal réglé peut rendre une application inutilisable à l\'échelle.')
speech('Comme on dit : "Optimiser sans mesurer, c\'est naviguer sans boussole." Merci pour votre attention — on est disponibles pour vos questions.')
separator()

# ═════════════════════════════════════════════════════════════════════════════
#  RÉCAP COMMANDES
# ═════════════════════════════════════════════════════════════════════════════
doc.add_page_break()
h1('📋  RÉCAP — Toutes les commandes et URLs')

h2('Démarrage')
cmd('cd C:\\Users\\Utilisateur\\gaming-performance-api')
cmd('docker compose up -d')
cmd('docker compose ps')

h2('Vérification que tout fonctionne')
url('http://localhost:8080/actuator/health    ← doit afficher  {"status":"UP"}')
url('http://localhost:9090                    ← Prometheus')
url('http://localhost:3000                    ← Grafana  (admin / admin)')
url('http://localhost:8090                    ← Kafka UI')

h2('Commandes pour la démo des anti-patterns')
cmd('docker logs gaming-api -f 2>&1 | Select-String "select"')
body('→ Affiche les requêtes SQL en temps réel (Ctrl+C pour arrêter)', indent=True)
cmd('docker logs gaming-api --tail 50 2>&1 | Select-String "ERROR|Exception"')
body('→ Affiche les erreurs récentes', indent=True)

h2('Requêtes Prometheus à taper')
cmd('jvm_memory_used_bytes')
cmd('http_server_requests_seconds_count')
cmd('hikaricp_connections_active')
cmd('http_server_requests_seconds_sum{uri="/api/dashboard"}')

h2('Arrêt propre à la fin')
cmd('docker compose down')

separator()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Gaming Performance API  —  Guide de présentation  —  2026')
r.font.size = Pt(9); r.italic = True
r.font.color.rgb = RGBColor(0xAA,0xAA,0xAA)

doc.save('/output/guide_presentation_complet.docx')
print('✅  Word généré !')

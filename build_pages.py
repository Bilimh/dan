"""Génère les pages HTML statiques du site DAN (dist/*.html).

Le résultat est du HTML ordinaire : on peut ensuite le modifier à la main.
"""
import html
import os
from PIL import Image

DIST = "/home/bilal/dan-officiel/dist"
PHOTOS = os.path.join(DIST, "assets/photos")

# nom : (texte alternatif / légende, rubrique de la galerie)
CATALOG = {
    "champ-aigrettes": ("Aigrettes au-dessus d’une parcelle fraîchement plantée", "champs"),
    "champ-rangs": ("Rangs de cultures irriguées au goutte-à-goutte", "champs"),
    "champ-piments": ("Rangs de piments à perte de vue", "champs"),
    "champ-horizon": ("Une parcelle du domaine, jusqu’à l’horizon", "champs"),
    "champ-paillage": ("Culture sur paillage, irriguée au goutte-à-goutte", "champs"),
    "plantation": ("Une équipe au travail dans une grande parcelle", "champs"),
    "pepiniere-plaques": ("Préparation des plaques de semis à la pépinière", "pepiniere"),
    "pepiniere-serre": ("Jeunes plants sous l’ombrière de la pépinière", "pepiniere"),
    "pepiniere-plants": ("Jeunes plants vigoureux sous ombrière", "pepiniere"),
    "repiquage": ("Repiquage de jeunes plants au champ", "pepiniere"),
    "verger-mangues": ("Jeunes mangues Kent sur un manguier du domaine", "produits"),
    "recolte-caisses": ("Une équipe de récolte devant les caisses remplies", "recoltes"),
    "recolte-mais": ("Récolte du maïs au champ", "recoltes"),
    "recolte-ensachage": ("Mise en sacs de la récolte", "recoltes"),
    "recolte-sacs": ("Sacs de récolte alignés au champ", "recoltes"),
    "oignons-champ": ("Sacs d’oignons rouges au champ", "produits"),
    "oignons-conteneur": ("Oignons chargés dans un conteneur", "produits"),
    "mais-sechage": ("Épis de maïs mis à sécher", "produits"),
    "mais-sacs": ("Sacs de maïs égrené", "produits"),
    "courge-butternut": ("Courge butternut ouverte", "produits"),
    "courge-coupe": ("Courges butternut fraîchement coupées", "produits"),
    "conditionnement-chaine": ("La chaîne de conditionnement des mangues", "conditionnement"),
    "conditionnement-tri": ("Contrôle des mangues sur la ligne de tri", "conditionnement"),
    "mangues-cartons": ("Mangues Kent conditionnées en cartons", "conditionnement"),
    "chargement-camion": ("Chargement d’un camion au départ du domaine", "conditionnement"),
    "elevage-vache": ("Une vache et son veau au domaine", "elevage"),
    "conditionnement-equipe": ("L’équipe réunie à la station de conditionnement", "equipes"),
    "equipe-partenaire": ("Aminata Dominique Diouf, directrice du domaine, avec un partenaire", "equipes"),
    "equipe-direction": ("Membres de l’équipe du domaine", "equipes"),
    "equipe-terrain": ("Une visite de terrain avec les équipes", "equipes"),
}
VIDEOS = {
    "piments": ("Plants de piments au domaine", "produits"),
    "elevage": ("Soins à un veau, à l’élevage du domaine", "elevage"),
}
GALLERY_TOPICS = [
    ("champs", "Les champs"), ("pepiniere", "Pépinière"), ("recoltes", "Récoltes"),
    ("produits", "Productions"), ("conditionnement", "Conditionnement"),
    ("elevage", "Élevage"), ("equipes", "Les équipes"),
]

SIZES = {}
for name in CATALOG:
    SIZES[name] = Image.open(os.path.join(PHOTOS, name + ".webp")).size


def e(text):
    return html.escape(text, quote=True)


def src(name, small=False):
    path = f"assets/photos/{name}-640.webp"
    if small and os.path.exists(os.path.join(DIST, path)):
        return path
    return f"assets/photos/{name}.webp"


def img(name, sizes="100vw", eager=False, cls="", alt=None, position=None):
    w, h = SIZES[name]
    alt = CATALOG[name][0] if alt is None else alt
    small = os.path.join(PHOTOS, name + "-640.webp")
    srcset = f' srcset="assets/photos/{name}-640.webp 640w, assets/photos/{name}.webp {w}w" sizes="{sizes}"' if os.path.exists(small) else ""
    load = ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    style = f' style="object-position:{position}"' if position else ""
    klass = f' class="{cls}"' if cls else ""
    return f'<img{klass} src="assets/photos/{name}.webp"{srcset} width="{w}" height="{h}" alt="{e(alt)}"{load}{style}>'


def zoomable(name, inner, cls="frame", caption=None):
    """Lien vers l'image entière : ouvre la visionneuse (et reste un lien sans JavaScript)."""
    cap = caption or CATALOG[name][0]
    return (f'<a class="{cls}" href="assets/photos/{name}.webp" data-lightbox data-caption="{e(cap)}" '
            f'data-alt="{e(CATALOG[name][0])}" aria-label="Agrandir : {e(cap)}">{inner}</a>')


def figure(name, sizes="100vw", caption=None, cls="", reveal=True, position=None):
    cap = caption or CATALOG[name][0]
    attrs = ' data-reveal' if reveal else ''
    return (f'<figure class="{cls}"{attrs}>{zoomable(name, img(name, sizes, position=position), caption=cap)}'
            f'<figcaption>{e(cap)}</figcaption></figure>')


def video(name, cls=""):
    alt = VIDEOS[name][0]
    return (f'<video class="{cls}" data-autoplay muted loop playsinline preload="none" poster="assets/photos/{name}-poster.webp" '
            f'aria-label="{e(alt)}"><source src="assets/photos/{name}.mp4" type="video/mp4"></video>')


# Adresse publique du site, sans « / » final (ex. "https://www.dan.sn"). Tant qu'elle est vide,
# les balises qui exigent une URL complète (aperçu de partage, sitemap) ne sont pas générées.
SITE_URL = ""
# Chemin du site sur le serveur : "/dan/" sur GitHub Pages (https://bilimh.github.io/dan/),
# "/" une fois le nom de domaine en place. Sert à la page 404, appelée depuis n'importe quelle adresse.
BASE_PATH = "/dan/"
PAGES = []

NAV = [
    ("a-propos.html", "Le domaine"), ("activites.html", "Nos activités"), ("valeurs.html", "Nos engagements"),
    ("organisation.html", "Les équipes"), ("galerie.html", "En images"),
]




# Flèches dessinées en SVG : les caractères ↗ ↓ ← → s'affichent en emoji sur certains téléphones.
# Dans le source, on continue d'écrire le caractère ; il est remplacé à la génération.
def _svg(path):
    return ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="{path}"/></svg>')


ICONS = {
    "↗": _svg("M7 17 17 7M8 7h9v9"),
    "↘": _svg("M7 7l10 10M17 8v9H8"),
    "↓": _svg("M12 5v14M6 13l6 6 6-6"),
    "←": _svg("M19 12H5M11 6l-6 6 6 6"),
    "→": _svg("M5 12h14M13 6l6 6-6 6"),
}


def social(filename, image):
    """Balises qui demandent une URL absolue : seulement si SITE_URL est renseignée."""
    if not SITE_URL:
        return ""
    url = f"{SITE_URL}/" if filename == "index.html" else f"{SITE_URL}/{filename}"
    image = image or "assets/photos/champ-aigrettes.webp"
    return (f'\n<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">'
            f'\n<meta property="og:image" content="{SITE_URL}/{image}">\n<meta name="twitter:card" content="summary_large_image">')


def page(filename, title, description, body, preload=None, home=False):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == filename else ""}>{label}</a>' for href, label in NAV
    )
    pre = f'\n<link rel="preload" as="image" href="{preload}">' if preload else ""
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Domaine Agricole de Néma">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">{social(filename, preload)}
<meta name="theme-color" content="#f7ae3e">
<link rel="icon" type="image/jpeg" href="assets/logo-dan.jpeg">
<link rel="preload" href="assets/fonts/jost.woff2" as="font" type="font/woff2" crossorigin>{pre}
<link rel="stylesheet" href="style.css">
<script src="main.js" defer></script>
</head>
<body class="{'home' if home else 'inner'}">
<a class="skip" href="#contenu">Aller au contenu</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="index.html" class="brand" aria-label="Domaine Agricole de Néma, accueil"><img src="assets/logo-dan.jpeg" alt="" width="273" height="103"></a>
    <nav id="nav" class="site-nav" aria-label="Navigation principale">{links}<a class="nav-contact" href="#contact">Contact</a></nav>
    <button id="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</header>
<main id="contenu">
{body}
</main>
<footer id="contact" class="site-footer">
  <div class="wrap">
    <div class="footer-main">
      <h2 data-words>Parlons de vos <span class="hl">projets agricoles.</span></h2>
      <div class="footer-contact" data-reveal>
        <a class="footer-cta" href="mailto:contact@dan.sn" data-magnet>Écrire au domaine <span aria-hidden="true">↗</span></a>
        <a href="tel:+221338898712">+221 33 889 87 12</a>
        <a href="mailto:contact@dan.sn">contact@dan.sn</a>
        <span>1, rue Ramez Bourgi · Sénégal</span>
      </div>
    </div>
    <nav class="footer-links" aria-label="Navigation de pied de page">{''.join(f'<a href="{h}">{l}</a>' for h, l in NAV)}</nav>
    <div class="footer-bottom"><span>© 2026 Domaine Agricole de Néma</span><span>La terre nous réunit.</span></div>
    <p class="legal-line">SA au capital de 150 000 000 FCFA · NINEA : 005136909 · RCCM : SN DKR 14431</p>
  </div>
</footer>
<dialog id="lightbox" class="lightbox" aria-label="Visionneuse d’images">
  <button class="lb-close" type="button" data-lb-close>Fermer</button>
  <figure><img data-lb-img alt=""><figcaption><span data-lb-caption></span><span data-lb-count></span></figcaption></figure>
  <button class="lb-btn lb-prev" type="button" data-lb-prev aria-label="Image précédente">←</button>
  <button class="lb-btn lb-next" type="button" data-lb-next aria-label="Image suivante">→</button>
</dialog>
</body>
</html>
"""
    if filename != "404.html":
        PAGES.append(filename)
    else:
        # En ligne, cette page est servie à n'importe quelle adresse (/a/b/c) : ses chemins relatifs
        # doivent partir de la racine du site. Ouverte comme fichier local, « / » désignerait la racine
        # du disque : on n'ajoute donc la base que sur un vrai serveur.
        doc = doc.replace("<head>\n", '<head>\n<meta name="robots" content="noindex">\n'
                          f'<script>if (location.protocol !== "file:") document.write(\'<base href="{BASE_PATH}">\');</script>\n', 1)
    for char, svg in ICONS.items():
        doc = doc.replace(char, svg)
    with open(os.path.join(DIST, filename), "w") as f:
        f.write(doc)


# --- Le médaillon : les photos dans un cercle, comme le baobab du logo, avec un texte qui tourne autour.
RING = "Domaine Agricole de Néma · Cultiver · Transformer · Transmettre · "


def roundel(photos, ring=RING, eager=True, cls=""):
    slides = []
    for i, (name, position) in enumerate(photos):
        w, h = SIZES[name]
        load = ' fetchpriority="high"' if (eager and i == 0) else ' loading="lazy" decoding="async"'
        slides.append(
            f'<img class="slide" data-slide data-label="{e(CATALOG[name][0])}" src="assets/photos/{name}.webp" '
            f'width="{w}" height="{h}" alt="{e(CATALOG[name][0])}"{load} style="object-position:{position}">'
        )
    dots = "".join(
        f'<button type="button" class="dot" data-bar aria-label="Photo {i + 1} sur {len(photos)}"><span></span></button>'
        for i in range(len(photos))
    ) if len(photos) > 1 else ""
    return f"""<div class="roundel {cls}" data-slides="2600">
  <div class="roundel-disc">{''.join(slides)}</div>
  <svg class="roundel-ring" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="ring-{cls or 'p'}" d="M100,100 m-88,0 a88,88 0 1,1 176,0 a88,88 0 1,1 -176,0"/></defs><text textLength="548" lengthAdjust="spacing"><textPath href="#ring-{cls or 'p'}" textLength="548" lengthAdjust="spacing">{e(ring)}</textPath></text></svg>
  <span class="roundel-sun" aria-hidden="true"></span>
  {f'<div class="roundel-dots">{dots}</div>' if dots else ''}
  <p class="roundel-caption" data-caption aria-live="polite"></p>
</div>"""


def page_hero(title, lede, photos, ring=RING):
    return f"""<section class="page-hero wrap">
  <div class="page-hero-copy">
    <h1 data-words>{title}</h1>
    <p class="lede" data-reveal>{lede}</p>
  </div>
  {roundel(photos, ring, cls="hero-roundel")}
</section>"""


def kicker(text):
    return f'<p class="kicker" data-reveal>{text}</p>'


def band(photo, title, text="", extra="", position="center"):
    """Grande photo qui s'ouvre en cercle au défilement, avec une carte orange posée dessus."""
    return f"""<section class="band" data-panel>
  <div class="band-media">{img(photo, "100vw", position=position)}</div>
  <div class="wrap band-inner"><div class="band-card" data-reveal><h2>{title}</h2>{f'<p>{text}</p>' if text else ''}{extra}</div></div>
</section>"""


def pill(name, position="center"):
    """Petite photo ronde glissée dans le texte (décorative : le texte dit déjà tout)."""
    return f'<span class="pill" aria-hidden="true"><img src="{src(name, small=True)}" alt="" loading="lazy" style="object-position:{position}"></span>'


# ---------------------------------------------------------------------------- accueil
CROPS = [
    ("Mangue Kent", "verger-mangues", "activites.html#mangue"),
    ("Oignon", "oignons-champ", "activites.html#cultures"),
    ("Maïs", "mais-sechage", "activites.html#cultures"),
    ("Piment", "champ-piments", "activites.html#cultures"),
    ("Courge", "courge-butternut", "activites.html#cultures"),
    ("Élevage", "elevage-vache", "activites.html#diversification"),
    ("Apiculture", None, "activites.html#diversification"),
    ("Pisciculture", None, "activites.html#diversification"),
]


def crop_index():
    rows = []
    for name, photo, href in CROPS:
        thumb = f'<span class="crop-thumb">{img(photo, "120px", alt="")}</span>' if photo else '<span class="crop-thumb crop-thumb--empty"></span>'
        data = f' data-preview="assets/photos/{photo}.webp"' if photo else ""
        rows.append(f'<li><a class="crop" href="{href}"{data}>{thumb}<span class="crop-name">{name}</span><span class="crop-go" aria-hidden="true">↗</span></a></li>')
    return "".join(rows)


PATH_STEPS = [
    ("La pépinière", "Sous ombrière, les jeunes plants prennent force avant de rejoindre le champ.", "pepiniere-plaques"),
    ("Au champ", "Les parcelles sont plantées et irriguées au goutte-à-goutte, pour maîtriser l’utilisation de l’eau.", "plantation"),
    ("La récolte", "Mangues, oignons, maïs : les équipes du domaine, renforcées par les saisonniers, récoltent à maturité.", "recolte-mais"),
    ("Au conditionnement", "Dans les stations du domaine, les fruits sont contrôlés, triés et mis en cartons.", "conditionnement-chaine"),
    ("Le départ", "Les récoltes prennent la route vers les marchés du Sénégal, d’Europe et d’Afrique.", "chargement-camion"),
]


def furrow():
    steps = "".join(
        f"""<li class="path-step" data-reveal>
      <div class="path-photo">{zoomable(p, img(p, "(max-width: 700px) 100vw, 34vw"))}</div>
      <div class="path-copy"><h3>{t}</h3><p>{txt}</p></div>
    </li>"""
        for t, txt, p in PATH_STEPS
    )
    return f"""<section class="path" aria-labelledby="path-title">
  <div class="wrap path-head">
    {kicker("Le chemin d’une récolte")}
    <h2 id="path-title" data-words>Une graine,<br>des mains, <span class="hl">un voyage.</span></h2>
  </div>
  <div class="wrap path-body" data-draw data-lightbox-group>
    <svg class="path-line" viewBox="0 0 100 1000" preserveAspectRatio="none" aria-hidden="true">
      <path pathLength="1" d="M50,0 C92,90 92,160 50,200 S8,310 50,400 S92,510 50,600 S8,710 50,800 S92,930 50,1000"/>
    </svg>
    <ol class="path-steps">{steps}</ol>
  </div>
</section>"""


def roundel_card(photo, title, text, href, link):
    return f"""<article class="engage" data-reveal>
      <div class="engage-disc">{img(photo, "(max-width: 700px) 70vw, 24vw")}</div>
      <h3>{title}</h3>
      <p>{text}</p>
      <a class="link" href="{href}">{link} <span aria-hidden="true">↗</span></a>
    </article>"""


MARQUEE_A = ["recolte-ensachage", "pepiniere-plants", "mais-sacs", "courge-coupe", "oignons-conteneur", "repiquage", "mangues-cartons"]
MARQUEE_B = ["champ-aigrettes", "conditionnement-tri", "pepiniere-serre", "recolte-sacs", "equipe-terrain", "champ-paillage", "elevage-vache"]


def marquee(names, reverse=False):
    first = "".join(zoomable(p, img(p, "320px"), cls="marquee-item") for p in names)
    # Deuxième passage identique pour une boucle continue ; ignoré par les lecteurs d'écran.
    second = "".join(
        zoomable(p, img(p, "320px", alt=""), cls="marquee-item").replace("<a ", '<a aria-hidden="true" tabindex="-1" ', 1)
        for p in names
    )
    return f'<div class="marquee{" marquee--reverse" if reverse else ""}"><div class="marquee-track">{first}{second}</div></div>'


HOME = f"""<section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-copy">
    <h1 id="hero-title" data-words>La terre<br>nous <span class="hl hl--draw">réunit.</span></h1>
    <p class="lede" data-reveal>Du verger aux marchés, une histoire agricole portée par les femmes et les hommes de Néma.</p>
    <div class="hero-actions" data-reveal>
      <a class="btn" href="#domaine" data-magnet>Entrer dans le domaine <span aria-hidden="true">↓</span></a>
      <a class="link" href="galerie.html">Le domaine en images <span aria-hidden="true">↗</span></a>
    </div>
  </div>
  {roundel([("champ-aigrettes", "40% 50%"), ("verger-mangues", "center 40%"), ("recolte-caisses", "center 35%"), ("champ-rangs", "center 60%"), ("conditionnement-chaine", "center 40%")], cls="hero-roundel")}
</section>

<section class="facts" aria-label="Le domaine en chiffres">
  <ul class="wrap facts-row">
    <li class="fact fact--sun" data-reveal><strong data-count="1996" data-raw="1">1996</strong><span>Création du domaine par Alioune Ndour Diouf</span></li>
    <li class="fact fact--leaf" data-reveal><strong data-count="19">19</strong><span>salariés permanents</span></li>
    <li class="fact fact--char" data-reveal><strong data-count="150">150</strong><span>saisonniers par jour au plus fort des récoltes</span></li>
    <li class="fact fact--ring" data-reveal><strong data-count="4">4</strong><span>conteneurs en chambre froide</span></li>
  </ul>
</section>

<section class="intro wrap" id="domaine" aria-labelledby="intro-title">
  <div class="intro-side">
    {kicker("Le Domaine Agricole de Néma")}
    <h2 class="intro-title" id="intro-title" data-words>Une histoire<br>qui prend racine.</h2>
    <dl class="intro-people" data-reveal>
      <div><dt>Fondateur</dt><dd>Alioune Ndour Diouf</dd></div>
      <div><dt>Directrice depuis 2014</dt><dd>Aminata Dominique Diouf</dd></div>
    </dl>
    <a class="link" href="a-propos.html" data-reveal>L’histoire du domaine <span aria-hidden="true">↗</span></a>
  </div>
  <p class="intro-text" data-reveal>Né vers 1996 d’une passion pour la terre {pill("champ-horizon", "center 70%")} le domaine a d’abord été <b>un maraîchage</b>. Puis sont venus <b>les manguiers Kent</b> {pill("verger-mangues")} les <b>stations de conditionnement</b> {pill("conditionnement-tri")} et <b>l’usine de transformation</b>. Aujourd’hui, ses récoltes {pill("oignons-conteneur")} voyagent du Sénégal jusqu’en <b>Europe et en Afrique</b>.</p>
</section>

<section class="crops-section" aria-labelledby="crops-title">
  <div class="wrap crops-grid">
    <div class="crops-head">
      {kicker("Nos productions")}
      <h2 id="crops-title" data-words>Ce qui pousse<br>à Néma.</h2>
      <p data-reveal>De l’arboriculture au maraîchage, de l’élevage à l’apiculture et à la pisciculture : des métiers complémentaires, encadrés par des responsables spécialisés.</p>
      <a class="link link--dark" href="activites.html" data-reveal>Toutes nos activités <span aria-hidden="true">↗</span></a>
    </div>
    <ul class="crop-list" data-preview-list>{crop_index()}</ul>
  </div>
  <div class="crop-preview" data-preview-box aria-hidden="true"><img alt=""></div>
</section>

{furrow()}

{band("champ-horizon", "Des terres, plusieurs horizons.", "Néma Nding, Keur Lamine Diamé et Kibik : le domaine est implanté dans les régions de Fatick et de Thiès, et s’étend vers Nguéniène.", '<a class="link link--dark" href="a-propos.html">Nos territoires <span aria-hidden="true">↗</span></a>', "center 72%")}

<section class="engagements wrap" aria-labelledby="engage-title">
  <div class="section-head">
    <div>{kicker("Nos engagements")}<h2 id="engage-title" data-words>Faire place <span class="hl">à l’avenir.</span></h2></div>
    <p data-reveal>Le développement du domaine s’appuie sur l’attention portée aux personnes, aux communautés et aux ressources.</p>
  </div>
  <div class="engage-grid">
    {roundel_card("champ-paillage", "Préserver les ressources", "Irrigation au goutte-à-goutte, énergie solaire et biogaz, protection raisonnée des cultures et plantations de manguiers qui contribuent au stockage du carbone.", "valeurs.html#environnement", "Notre démarche")}
    {roundel_card("pepiniere-serre", "Respecter les personnes", "Des engagements fondés sur le respect des droits des collaborateurs, les règles sociales en vigueur et la couverture prévue pour les équipes.", "valeurs.html#collaborateurs", "Nos engagements sociaux")}
    {roundel_card("recolte-caisses", "Grandir avec les communautés", "Participation aux activités de vacances des jeunes, dons aux postes de santé et soutien aux cérémonies religieuses et aux activités culturelles.", "valeurs.html#communautes", "Nos actions locales")}
  </div>
</section>

<section class="team wrap" aria-labelledby="team-title" data-lightbox-group>
  <div class="team-media">
    {figure("equipe-partenaire", "(max-width: 700px) 100vw, 46vw", "Aminata Dominique Diouf, directrice du domaine, avec un partenaire.", "team-main", position="65% center")}
    <div class="team-badge" aria-hidden="true"><span>Depuis</span><strong>2014</strong><span>à la direction</span></div>
  </div>
  <div class="team-copy">
    {kicker("Celles et ceux qui font DAN")}
    <h2 id="team-title" data-words>Un savoir-faire <span class="hl">en partage.</span></h2>
    <p class="lede" data-reveal>Depuis 2014, Aminata Dominique Diouf assure la direction du domaine. Elle est secondée par Alioune Badara Sylla, ingénieur agronome, à la tête d’une équipe technique et d’ouvriers saisonniers.</p>
    <a class="link" href="organisation.html" data-reveal>Découvrir les équipes <span aria-hidden="true">↗</span></a>
  </div>
</section>

<section class="wall" aria-labelledby="wall-title" data-lightbox-group>
  <div class="wrap section-head">
    <div>{kicker("En images")}<h2 id="wall-title" data-words>Une saison <span class="hl">au domaine.</span></h2></div>
    <a class="btn btn--ghost" href="galerie.html" data-reveal>Toute la galerie <span aria-hidden="true">↗</span></a>
  </div>
  {marquee(MARQUEE_A)}
  {marquee(MARQUEE_B, reverse=True)}
</section>"""

page("index.html", "Domaine Agricole de Néma — Cultiver, transformer, transmettre",
     "Depuis 1996, le Domaine Agricole de Néma associe production agricole, conditionnement, transformation et commercialisation au Sénégal.",
     HOME, preload="assets/photos/champ-aigrettes.webp", home=True)


# ---------------------------------------------------------------------------- le domaine
TIMELINE = [
    ("1996", "Vers 1996", "Les premiers sillons", "Création du domaine et démarrage des activités maraîchères.", "plantation"),
    ("2000", "Vers 2000", "Les manguiers Kent", "Plantation des premiers manguiers de variété Kent, qui deviendront un axe majeur de l’activité arboricole.", "verger-mangues"),
    ("2006", "2006–2007", "Le conditionnement et l’export", "Construction de la première station de conditionnement à Noflaye, dans la commune de Sangalkam. Premier certificat pour l’exportation de mangues vers l’Europe, puis expédition des premiers conteneurs.", "mangues-cartons"),
    ("2010", "2010–2011", "De nouvelles terres à Kibik", "Acquisition de terres à Kibik, dans la commune de Sandiara, et construction d’une deuxième station de conditionnement.", "champ-rangs"),
    ("2014", "2014–2015", "Une nouvelle direction", "Aminata Dominique Diouf prend la direction du domaine. DAN acquiert de nouvelles terres à Keur Samba Guèye.", "equipe-partenaire"),
    ("2020", "2020–2022", "Transformer sur place", "Construction d’une usine de transformation de mangues et de produits dérivés, puis d’un centre de conditionnement équipé d’une chambre froide pouvant accueillir quatre conteneurs.", "conditionnement-chaine"),
    ("2025", "Depuis 2025", "Un nouveau centre à Nguéniène", "Construction d’un nouveau centre de conditionnement dans la commune de Nguéniène, vers Fadial.", "chargement-camion"),
]
timeline_html = "".join(
    f"""<li class="year" data-reveal>
    <span class="year-big" aria-hidden="true">{big}</span>
    <div class="year-photo">{zoomable(p, img(p, "(max-width: 700px) 100vw, 26vw"))}</div>
    <div class="year-copy"><p class="year-date">{date}</p><h3>{t}</h3><p>{txt}</p></div>
  </li>"""
    for big, date, t, txt, p in TIMELINE
)
LOCATIONS = [
    ("Néma Nding", "Commune de Toubacouta · Département de Foundiougne · Région de Fatick"),
    ("Keur Lamine Diamé", "Commune de Keur Samba Guèye · Département de Foundiougne · Région de Fatick"),
    ("Kibik", "Commune de Sandiara · Département de Mbour · Région de Thiès"),
]
ABOUT = f"""{page_hero("La terre.<br><span class=\"hl\">Et le temps.</span>", "Depuis près de trois décennies, le Domaine Agricole de Néma grandit avec ses terres, ses équipes et ses productions.", [("champ-horizon", "center 70%"), ("plantation", "center"), ("verger-mangues", "center 40%")])}
<section class="wrap page-section">
  <p class="statement" data-reveal>Fondé vers 1996 par Alioune Ndour Diouf, DAN associe production agricole, conditionnement, transformation et commercialisation. Son histoire s’écrit au fil des plantations, des outils de travail et des nouveaux territoires.</p>
  <ol class="years" aria-label="Les étapes de développement" data-lightbox-group>{timeline_html}</ol>
</section>
{band("equipe-terrain", "La croissance du domaine s’appuie sur l’engagement des équipes.", position="center 35%")}
<section class="wrap page-section">
  <div class="section-head"><div>{kicker("Nos territoires")}<h2 data-words>Des terres, <span class="hl">plusieurs horizons.</span></h2></div><p data-reveal>Le domaine est implanté dans plusieurs communes des régions de Fatick et de Thiès. Ses activités s’étendent également dans la commune de Nguéniène.</p></div>
  <div class="locations">{''.join(f'<article class="location" data-reveal><span class="location-pin" aria-hidden="true"></span><h3>{n}</h3><p>{d}</p></article>' for n, d in LOCATIONS)}</div>
</section>"""
page("a-propos.html", "Le domaine — Domaine Agricole de Néma",
     "L’histoire du Domaine Agricole de Néma depuis 1996 : plantations, conditionnement, transformation et territoires.",
     ABOUT, preload="assets/photos/champ-horizon.webp")


# ---------------------------------------------------------------------------- activités
def duo(main, second, caption_main, caption_second, sizes_main="(max-width: 700px) 100vw, 34vw", video_main=None):
    first = (f'<figure class="duo-a" data-reveal>{video(video_main)}<figcaption>{e(caption_main)}</figcaption></figure>'
             if video_main else figure(main, sizes_main, caption_main, "duo-a"))
    return f'<div class="duo" data-lightbox-group>{first}{figure(second, "(max-width: 700px) 60vw, 20vw", caption_second, "duo-b")}</div>'


ACTIVITIES = f"""{page_hero("Cultiver.<br><span class=\"hl\">Valoriser.</span>", "Du verger à la transformation, des productions agricoles reliées aux marchés.", [("champ-rangs", "center 60%"), ("mangues-cartons", "center"), ("oignons-champ", "center")])}

<section id="mangue" class="wrap split">
  {duo("verger-mangues", "mangues-cartons", "Au verger, les mangues prennent forme.", "Mangues Kent en cartons, prêtes à partir.")}
  <div class="split-copy">
    {kicker("Au cœur du verger")}
    <h2 data-words>La mangue <span class="hl">Kent.</span></h2>
    <p data-reveal>Plantés à partir des années 2000, les manguiers Kent occupent une place centrale dans les productions du domaine. La variété est appréciée pour sa chair douce et juteuse.</p>
    <p data-reveal>L’ensoleillement et la pluviométrie de la zone favorisent la production. La précocité des récoltes permet d’envisager les premières disponibilités à l’export dès la mi-mai ; volumes et calendrier se précisent pour chaque campagne.</p>
  </div>
</section>

<section id="cultures" class="wrap chapter">
  <div class="section-head"><div>{kicker("Productions complémentaires")}<h2 data-words>Faire vivre <span class="hl">la diversité.</span></h2></div><p data-reveal>Le maraîchage et d’autres cultures complètent l’arboriculture. Les productions mentionnées par le domaine comprennent notamment les oignons et le maïs.</p></div>
  <div class="crops" data-lightbox-group>
    {figure("oignons-champ", "(max-width: 700px) 100vw, 46vw", "Récolte d’oignons au champ.", "c-wide")}
    <figure class="c-video" data-reveal>{video("piments")}<figcaption>Les piments, au champ.</figcaption></figure>
    {figure("mais-sechage", "(max-width: 700px) 100vw, 24vw", "Le maïs mis à sécher.", "c-tall")}
    {figure("courge-coupe", "(max-width: 700px) 100vw, 46vw", "Des courges fraîchement coupées.", "c-wide2")}
    {figure("mais-sacs", "(max-width: 700px) 100vw, 24vw", "Le maïs égrené, en sacs.", "c-small")}
  </div>
</section>

{band("pepiniere-plaques", "Préparer. Transformer.", "Le soin apporté à chaque étape, de la pépinière à la station de conditionnement.")}

<section id="valorisation" class="wrap chapter">
  <div class="section-head"><div>{kicker("Conditionnement &amp; transformation")}<h2 data-words>Des stations <span class="hl">aux marchés.</span></h2></div>
    <div data-reveal><p>Depuis la première station de conditionnement construite à Noflaye, DAN a développé ses équipements pour accompagner la commercialisation des récoltes. Un second site a été construit à Kibik.</p><p>Entre 2020 et 2022, le domaine a construit une usine de transformation de mangues et de produits dérivés ainsi qu’un centre de conditionnement doté d’une chambre froide d’une capacité de quatre conteneurs.</p></div>
  </div>
  <div class="trio" data-lightbox-group>
    {figure("conditionnement-chaine", "(max-width: 700px) 100vw, 33vw", "La chaîne de conditionnement.")}
    {figure("conditionnement-tri", "(max-width: 700px) 100vw, 33vw", "Le contrôle des fruits sur la ligne de tri.")}
    {figure("oignons-conteneur", "(max-width: 700px) 100vw, 33vw", "Les oignons chargés en conteneur.")}
  </div>
  <div data-lightbox-group>{figure("chargement-camion", "100vw", "Au départ du domaine, la récolte prend la route.", "wide-photo")}</div>
</section>

<section id="diversification" class="wrap split split--reverse">
  {duo(None, "elevage-vache", "Un aperçu de l’activité d’élevage.", "Une vache et son veau au domaine.", video_main="elevage")}
  <div class="split-copy">
    {kicker("Des métiers complémentaires")}
    <h2 data-words>Élargir <span class="hl">les savoir-faire.</span></h2>
    <p data-reveal>L’arboriculture et le maraîchage s’inscrivent dans une activité agricole plus large. Les équipes du domaine couvrent également l’apiculture, l’élevage, la pisciculture et la transformation.</p>
    <p data-reveal>Ces fonctions spécialisées sont portées par des responsables de production animale, d’apiculture, de pisciculture et de transformation.</p>
  </div>
</section>

<section id="projets" class="wrap chapter projects">
  <div class="section-head"><div>{kicker("Les prochaines étapes")}<h2 data-words>Continuer <span class="hl">à grandir.</span></h2></div></div>
  <div class="project-grid">
    <article class="project" data-reveal><span class="project-dot" aria-hidden="true"></span><h3>Diversifier</h3><p>Étendre et diversifier les productions, notamment par l’introduction de nouvelles variétés de mangues et d’autres cultures maraîchères.</p></article>
    <article class="project" data-reveal><span class="project-dot" aria-hidden="true"></span><h3>Innover</h3><p>Des outils de surveillance des cultures et d’analyse des données, avec des pistes comme les drones.</p></article>
    <article class="project" data-reveal><span class="project-dot" aria-hidden="true"></span><h3>Former</h3><p>Des formations pour le personnel et les agriculteurs locaux.</p></article>
    <article class="project" data-reveal><span class="project-dot" aria-hidden="true"></span><h3>Construire</h3><p>Depuis 2025, un nouveau centre de conditionnement est en construction dans la commune de Nguéniène, vers Fadial.</p></article>
  </div>
</section>"""
page("activites.html", "Nos activités — Domaine Agricole de Néma",
     "Mangue Kent, maraîchage, conditionnement, transformation et élevage : les activités du Domaine Agricole de Néma.",
     ACTIVITIES, preload="assets/photos/champ-rangs.webp")


# ---------------------------------------------------------------------------- engagements
VALUES = [
    ("Qualité &amp; rigueur", "Des exigences de production, de récolte et de conditionnement au service de la qualité et de la sécurité alimentaire."),
    ("Respect des personnes", "Le respect des droits des collaborateurs et des règles sociales en vigueur au Sénégal."),
    ("Responsabilité environnementale", "Des pratiques agricoles durables et une gestion raisonnée des ressources."),
    ("Ancrage local &amp; solidarité", "Une contribution à la vie sociale, sanitaire et culturelle des communautés où le domaine est implanté."),
    ("Innovation &amp; savoir-faire", "L’expérience des équipes associée à l’amélioration des techniques agricoles."),
    ("Traçabilité", "Des systèmes de suivi permettent de retracer le parcours des mangues, du verger jusqu’à leur commercialisation."),
]
ENV = [
    ("Préserver l’eau.", "L’irrigation au goutte-à-goutte accompagne la production et maîtrise l’utilisation de l’eau."),
    ("Mobiliser des énergies renouvelables.", "L’énergie solaire et le biogaz sont intégrés à la politique agricole du domaine."),
    ("Raisonner la protection des cultures.", "Le domaine privilégie une utilisation raisonnée des pesticides et les bonnes pratiques agricoles."),
    ("Valoriser les plantations.", "Les plantations de manguiers contribuent au stockage du carbone."),
]
VALUES_PAGE = f"""{page_hero("Prendre soin.<br><span class=\"hl\">Faire grandir.</span>", "La qualité des produits, le respect des personnes et la préservation des ressources guident le développement du domaine.", [("champ-aigrettes", "40% 50%"), ("champ-paillage", "center"), ("recolte-caisses", "center 35%")])}
<section class="wrap page-section">
  <p class="statement" data-reveal>Produire et valoriser des produits agricoles de qualité, approvisionner les marchés et contribuer au développement économique local, tout en préservant les ressources naturelles.</p>
  <div class="value-grid">{''.join(f'<article class="value" data-reveal><h2>{t}</h2><p>{d}</p></article>' for t, d in VALUES)}</div>
</section>

<section id="environnement" class="wrap split">
  {duo("champ-paillage", "champ-rangs", "Culture sur paillage, irriguée au goutte-à-goutte.", "Des lignes d’irrigation au pied des cultures.")}
  <div class="split-copy">
    {kicker("Envers l’environnement")}
    <h2 data-words>Préserver <span class="hl">les ressources.</span></h2>
    <ul class="checks">{''.join(f'<li data-reveal><strong>{t}</strong> {d}</li>' for t, d in ENV)}</ul>
  </div>
</section>

{band("recolte-ensachage", "Travailler dans le respect.", "DAN exerce ses activités dans le respect des lois et règlements du Sénégal ainsi que des conventions collectives en vigueur. L’entreprise assure les cotisations sociales et la couverture maladie prévues pour ses collaborateurs. Le domaine compte dix-neuf salariés permanents ; selon les périodes de production et de récolte, les effectifs saisonniers peuvent atteindre cent cinquante personnes par jour, sur des périodes de trois à six mois.", position="center 30%").replace('<section class="band"', '<section class="band" id="collaborateurs"')}

<section id="communautes" class="wrap split split--reverse">
  {duo("recolte-caisses", "pepiniere-plaques", "Une équipe de récolte devant les caisses remplies.", "À la pépinière, un travail d’équipe.")}
  <div class="split-copy">
    {kicker("Envers les communautés")}
    <h2 data-words>Grandir <span class="hl">ensemble.</span></h2>
    <p data-reveal>Le domaine contribue à l’épanouissement socioculturel des communautés de ses zones d’activité. Cet engagement se traduit par des actions concrètes :</p>
    <ul class="checks">
      <li data-reveal>Participation aux activités de vacances des jeunes.</li>
      <li data-reveal>Dons aux postes de santé.</li>
      <li data-reveal>Soutien aux cérémonies religieuses et aux activités culturelles.</li>
    </ul>
  </div>
</section>

<section class="wrap chapter" id="certifications">
  <div class="section-head"><div>{kicker("Qualité &amp; reconnaissance")}<h2 data-words>Des exigences <span class="hl">suivies.</span></h2></div>
    <div data-reveal>
      <ul class="badges" aria-label="Référentiels cités"><li>GLOBALG.A.P.</li><li>Tesco Nurture</li><li>GRASP</li><li>SMETA</li></ul>
      <p>La présentation du domaine cite GLOBALG.A.P., Tesco Nurture et GRASP, ainsi que les audits sociaux SMETA, dans le cadre de ses démarches de qualité et de responsabilité sociale.</p>
      <p>La qualité, la traçabilité et la sécurité alimentaire s’inscrivent dans une démarche suivie tout au long du parcours des produits.</p>
    </div>
  </div>
</section>"""
page("valeurs.html", "Nos engagements — Domaine Agricole de Néma",
     "Qualité, respect des personnes, préservation des ressources et ancrage local : les engagements du Domaine Agricole de Néma.",
     VALUES_PAGE, preload="assets/photos/champ-aigrettes.webp")


# ---------------------------------------------------------------------------- équipes
ORG = [
    ("direction", "Direction", "La direction pilote l’activité et son développement.", ["Président du conseil d’administration (PCA)", "Directrice générale (DG)", "Directeur général adjoint (DGA)"]),
    ("production", "Production &amp; suivi technique", "Des fonctions dédiées à la conduite des productions et au suivi des cultures.", ["Direction de la production", "Chefs de périmètres", "Chefs de culture", "Responsable phytosanitaire"]),
    ("transformation", "Transformation", "Une équipe dédiée à la valorisation des récoltes et aux produits dérivés de la mangue.", ["Responsable de la transformation"]),
    ("activites", "Activités spécialisées", "Des responsables encadrent les activités complémentaires du domaine.", ["Responsable de l’apiculture", "Responsable de la pisciculture", "Responsable de la production animale"]),
    ("qualite", "Administration &amp; qualité", "Des fonctions support contribuent à la gestion et au suivi des pratiques du domaine.", ["Responsable administratif et financier (RAF)", "Responsable qualité, hygiène, sécurité et environnement (RQHSE)"]),
]
ORG_PAGE = f"""{page_hero("Des femmes.<br><span class=\"hl\">Des hommes.</span>", "Une organisation qui relie direction, métiers agricoles, transformation et fonctions support.", [("equipe-terrain", "center 35%"), ("recolte-caisses", "center 35%"), ("conditionnement-chaine", "center 40%")])}
<section class="wrap split leader">
  {duo("equipe-partenaire", "equipe-direction", "Aminata Dominique Diouf, directrice du domaine, avec un partenaire.", "Membres de l’équipe du domaine.")}
  <div class="split-copy">
    {kicker("La direction")}
    <h2 data-words>Aminata <span class="hl">Dominique Diouf.</span></h2>
    <p class="lede" data-reveal>Depuis 2014, Aminata Dominique Diouf assure la direction du Domaine Agricole de Néma. Elle est secondée par Alioune Badara Sylla, ingénieur agronome, à la tête d’une équipe technique et d’ouvriers saisonniers.</p>
  </div>
</section>

<section class="wrap page-section">
  <div class="section-head"><div>{kicker("Les fonctions")}<h2 data-words>Une organisation <span class="hl">claire.</span></h2></div></div>
  <div class="org">{''.join(f'<article class="org-unit" id="{i}" data-reveal><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></article>' for i, t, d, items in ORG)}</div>
</section>

{band("recolte-sacs", "Le partage d’expérience accompagne la vie des équipes.")}"""
page("organisation.html", "Les équipes — Domaine Agricole de Néma",
     "Direction, production, transformation et fonctions support : l’organisation du Domaine Agricole de Néma.",
     ORG_PAGE, preload="assets/photos/equipe-terrain.webp")


# ---------------------------------------------------------------------------- galerie
items = []
for name, (alt, topic) in CATALOG.items():
    items.append(
        f'<figure class="g-item" data-item="{topic}" data-reveal>'
        f'{zoomable(name, img(name, "(max-width: 700px) 50vw, 25vw"), cls="g-link")}'
        f'<figcaption>{e(alt)}</figcaption></figure>'
    )
for name, (alt, topic) in VIDEOS.items():
    items.append(f'<figure class="g-item g-video" data-item="{topic}" data-reveal>{video(name)}<figcaption>{e(alt)}</figcaption></figure>')
filters = '<button type="button" class="filter" data-filter="all" aria-pressed="true">Tout voir</button>' + "".join(
    f'<button type="button" class="filter" data-filter="{k}" aria-pressed="false">{v}</button>' for k, v in GALLERY_TOPICS
)
GALLERY = f"""<section class="wrap gallery-head">
  <h1 data-words>Une saison <span class="hl">au domaine.</span></h1>
  <p class="lede" data-reveal>Des champs à la station de conditionnement, les images du travail des équipes de Néma.</p>
</section>
<section class="wrap gallery" data-gallery data-lightbox-group aria-label="Galerie">
  <div class="gallery-bar"><div class="filters" role="group" aria-label="Filtrer les images">{filters}</div><span class="gallery-count" data-count-label aria-live="polite">{len(items)} images</span></div>
  <div class="g-grid">{''.join(items)}</div>
</section>"""
page("galerie.html", "En images — Domaine Agricole de Néma",
     "Champs, pépinière, récoltes, conditionnement, élevage et équipes : le Domaine Agricole de Néma en images.",
     GALLERY)

print("pages générées")


# ---------------------------------------------------------------------------- 404 et fichiers de déploiement
NOT_FOUND = f"""<section class="wrap not-found">
  {roundel([("champ-horizon", "center 70%")], ring="Page introuvable · Retour au domaine · ", eager=True, cls="nf-roundel")}
  <div>
    <h1 data-words>Ce chemin <span class="hl">ne mène nulle part.</span></h1>
    <p class="lede" data-reveal>La page demandée n’existe pas ou a été déplacée.</p>
    <a class="btn" href="index.html" data-reveal>Retour à l’accueil ↗</a>
  </div>
</section>"""
page("404.html", "Page introuvable — Domaine Agricole de Néma", "Cette page n’existe pas.", NOT_FOUND)

with open(os.path.join(DIST, "robots.txt"), "w") as f:
    f.write("User-agent: *\nAllow: /\n" + (f"Sitemap: {SITE_URL}/sitemap.xml\n" if SITE_URL else ""))
if SITE_URL:
    urls = "".join(f"  <url><loc>{SITE_URL}/{'' if p == 'index.html' else p}</loc></url>\n" for p in PAGES)
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
print("404, robots.txt" + (", sitemap.xml" if SITE_URL else " (sitemap : renseigner SITE_URL)"))

# Domaine Agricole de Néma — Code source

Version du site avec section contact regroupée, téléphone et contact@dan.com.

## Utilisation
Ouvrir dist/index.html dans un navigateur. Pour un serveur local :

    cd dist
    python -m http.server 8000

Puis ouvrir http://localhost:8000. Aucun build ni installation npm nécessaire.

## Contenu
- dist/ : toutes les pages HTML, style.css, scripts, polices et médias.
- references-design/ : sauvegarde des anciens bandeaux verts.

## Photos et mouvements
- dist/assets/photos/ : la photothèque du site, triée et nommée par sujet (champ-, pepiniere-, recolte-,
  conditionnement-, equipe-…). Le filigrane du téléphone a été retiré par recadrage ; chaque photo existe
  en taille d'origine et en 640 px. Les originaux restent dans dist/assets/.
- dist/main.js : les animations (apparitions, titres mot à mot, récit « du champ au conteneur », rail des
  productions, panneaux qui s'ouvrent, galerie et visionneuse), sans bibliothèque. Elles sont désactivées
  quand le visiteur demande moins d'animations ; sans JavaScript, tout reste lisible.
- dist/galerie.html : toutes les images, filtrables par thème, avec visionneuse plein écran.

## Principes de mise en page
- Couleurs du logo : orange mangue (#f7ae3e), vert feuille (#78ae44), anthracite (#25282b), fond crème.
- Formes du logo : le cercle du baobab (médaillons photo) et le sillon orange (chemin d'une récolte).
- Une seule police, Jost, hébergée dans dist/assets/fonts (licence SIL OFL).
- L'ancienne version du site reste consultable dans l'historique git (commit aa41cb8).
La photo de la vache a été retouchée par IA à la demande du propriétaire.

## Régénérer les pages
Les pages HTML sont produites par `build_pages.py` (textes, photos, liens) :

    python3 build_pages.py

Il demande Pillow (`pip install pillow`) pour lire la taille des photos. Les retouches de style se font
directement dans dist/style.css, les animations dans dist/main.js.

## Mettre en ligne
En attendant le nom de domaine, le site est publié sur GitHub Pages : https://bilimh.github.io/dan/
Chaque envoi sur la branche main republie automatiquement dist/ (.github/workflows/pages.yml).
Le jour du nom de domaine : passer BASE_PATH à "/" et renseigner SITE_URL dans build_pages.py,
relancer le script, puis déclarer le domaine dans Settings › Pages du dépôt.

Le dossier à publier est `dist/` : il est autonome (aucune compilation).
- Avant la mise en ligne, renseigner `SITE_URL` en haut de build_pages.py (ex. "https://www.dan.sn") puis
  relancer le script : il ajoute l'aperçu de partage (réseaux sociaux), l'adresse canonique et sitemap.xml.
- Ne pas laisser dans dist/ les documents de travail (Presentation_DAN_….docx, assets/images_officiels/) :
  tout ce qui est dans dist/ devient public.
- Netlify ou Cloudflare Pages : dossier de publication `dist`, pas de commande de build. dist/_headers
  règle la mise en cache et quelques en-têtes de sécurité ; dist/404.html sert de page introuvable.
- Autre hébergeur (serveur classique, cPanel) : envoyer le contenu de dist/ à la racine du site et
  déclarer 404.html comme page d'erreur.

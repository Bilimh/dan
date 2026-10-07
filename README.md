# Domaine Agricole de Néma — Code source

Version du site avec section contact regroupée, téléphone et contact@dan.com.

## Utilisation
Ouvrir dist/index.html dans un navigateur. Pour un serveur local :

    cd dist
    python -m http.server 8000

Puis ouvrir http://localhost:8000. Aucun build ni installation npm nécessaire.

## Contenu
- dist/ : toutes les pages HTML, style.css, scripts, polices et médias.
- dist-avant-refonte/ : le site tel qu'il était avant la refonte (à ne pas mettre en ligne).
- references-design/ : sauvegarde des anciens bandeaux verts.

## Principes de mise en page (refonte)
- Lignes droites, fond blanc, filets fins ; un seul aplat vert (la section contact).
- Grille de 13 colonnes partagée en 8 / 5 (nombre d'or), en alternance d'une section à l'autre.
- Espacements sur la suite de Fibonacci : 8, 13, 21, 34, 55, 89, 144 px (variables --s1 à --s7 dans style.css).
- Polices hébergées dans dist/assets/fonts : Bodoni Moda (titres) et Jost (texte), licence SIL OFL.

Le formulaire de contact désactivé est conservé dans dist-avant-refonte/index.html.
La photo de la vache a été retouchée par IA à la demande du propriétaire.

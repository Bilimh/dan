# Domaine Agricole de Néma — Code source

Version du site avec section contact regroupée, téléphone et contact@dan.com.

## Utilisation
Ouvrir dist/index.html dans un navigateur. Pour un serveur local :

    cd dist
    python -m http.server 8000

Puis ouvrir http://localhost:8000. Aucun build ni installation npm nécessaire.

## Contenu
- dist/ : toutes les pages HTML, style.css, scripts, polices et médias.
- dist-avant-refonte/ : l'ancienne version du site (à ne pas mettre en ligne).
- references-design/ : sauvegarde des anciens bandeaux verts.

## Principes de mise en page
- Lignes droites, fond blanc, filets fins ; un seul aplat vert (la section contact).
- Polices hébergées dans dist/assets/fonts : Bodoni Moda (titres) et Jost (texte), licence SIL OFL.

Le formulaire de contact désactivé est conservé dans dist-avant-refonte/index.html.
La photo de la vache a été retouchée par IA à la demande du propriétaire.

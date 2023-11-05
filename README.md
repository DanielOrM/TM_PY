# TM_PY
GIT REPOSITORY: https://github.com/DanielOrM/TM_PY.git

COMMENT LANCER LE JEU:
    - installez conda 
    - lancez votre IDE et ouvrez le dossier "TM" 
    - ouvrez un terminal bash:
        - cd mon_nom_est (si nécessaire)
        - ./launch_game.sh

INTÉRACTIONS GÉNÉRALES POSSIBLES:
    - motion (mouvement de souris):
        - obtient position x,y de la souris
        - appelle func "events_to_check"
    - click-gauche (intéragit avec certains objets)
    - e (intéragit avec certains objets)
    - click-droit (seulement quand appareil photo pris)
        - appuyé: initialise la prise de photos 
        - drag: crée rectangle pour prendre une photo
        - relâché: enregistre la photo dans l'album
    - middle click:
        - ouvre album photos
            - album photo:
                - appuyer sur flèche rouge gauche (tourne la page vers la gauche)
                - appuyer sur flèche rouge droite (tourne la page vers la droite)
                - 4 photos max à chaque 2 pages
    - a:
        - va à gauche
    - d: 
        - va à droite

INTÉRACTIONS SPÉCIFIQUES:
    - Cahier de dessin
        - click gauche:
            - traçage de points pour faire un dessin

STRUCTURE PIÈCES:
    - résumé sous func "events_to_check" de la classe GameEventHandler

NOTES IMPORTANTES:
    - éviter de lancer deux dialogues de suite, cela va les "fusioner"
    - ne pas prendre une photo de bas en haut OU de droite à gauche
# TM_PY
GIT REPOSITORY: https://github.com/DanielOrM/TM_PY.git

COMMENT LANCER LE JEU:
    - veuillez d'aborder vérifier que votre OS est windows (cause: global_var.py)
    - installez conda
    - lancez votre IDE et ouvrez le dossier "TM_PY-master"
    - dans le terminal:
        - conda env create -f "requirements.yml"
            - il est possible qu'il que pygame, opencv, et PIL ne soient pas installé
                - pip install pygame
                - pip install opencv-python
                - pip install Pillow
        - conda activate tm_env
        - python .\mon_nom_est.py

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
    - éviter de lancer deux dialogues de suite, cela va les "fusioner" (ou juste enchâiner des actions à la seconde près)
    - pour le dessin après celui du loup-garou, le label 13 cache le point 13. Il faut quand même passer par-dessus
      pour que cela le prenne en compte.
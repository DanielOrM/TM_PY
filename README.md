# TM_PY
GIT REPOSITORY: https://github.com/DanielOrM/TM_PY.git

COMMENT LANCER LE JEU:
    - lancez votre IDE et ouvrez le dossier "TM" (donc sous-dossier: mon_nom_est)
    - ouvrez dossier mon_nom_est
    - dans le terminal écrivez:
        - _cd mon_nom_est_
        - _python mon_nom_est.py_


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
    - éviter de lancer deux intéractions en même temps (par ex: texte défilant), SURTOUT DU MEME GENRE
    - ne pas prendre une photo de bas en haut OU de droite à gauche
    - ne pas appuyer plusieurs fois de manière consécutive sur les touches a OU d pour changer de pièce
    - redémarrer le jeu si les intéractions avec les pièces ne se fait plus correctement 
        - (problème avec numérotation pyimage dans "events_to_check")
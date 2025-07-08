

README - Projet Python de génération de motifs
#########################################################

Description :

Application web développée en Python (Flask) permettant de générer des motifs géométriques (formes répétitives, spirales...) seulement avec turtle, à partir de paramètres choisis par l'utilisateur via une interface web.


########################################################

Structure du projet :

- app.py              : Lance le serveur Flask et gère les routes / formulaires
- geometry.py         : Contient toute la logique de dessin (avec turtle)
- templates/ main.html : Interface HTML utilisateur
- static/ style.css    : CSS de l'interface
- static/ shape.png    : Image générée 
- static/ shape.eps    : Version EPS temporaire pour Pillow (puis transformé en png)


######################################################

Dépendances :

- Python 3.8+
- Flask
- Pillow (PIL)
- tkinter (inclus avec Python)
- environnement venv

#####################################################

Lancer l'application :

1. - avoir python d'installé
   - puis pip install flask pillow pour les dépendances
   - un environnement venv : py -m venv .venv
   - .venv\Scripts\activate ou source .venv/bin/activate
et   reinstaller les dépendances dans le venv :  pip install flask pillow
  
2. Exécuter l’application :
   flask run ou python app.py (ou python3 app.py) 

3. Accéder à l’interface depuis le navigateur :
   http://127.0.0.1:5000


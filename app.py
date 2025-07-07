import os
import time
from flask import Flask, render_template, request
from geometry import *

# Instanciation de l'application Flask
app = Flask(__name__)

@app.route('/')
def main():
    
    # Route principale de l'application.
    # Affiche simplement la page HTML de base avec le formulaire.
    
    return render_template('main.html')

@app.route('/submit', methods=['POST'])
def submit():
    
    # Route qui gère la soumission du formulaire.
    # Récupère les paramètres envoyés par l'utilisateur et appelle
    # la génération de motif correspondante.
    
    motif_type = request.form.get("motif_type", "repetitive")

    if motif_type == "random":
        # génération aléatoire complète (pas besoin de paramètres)
        menu_generate(0, 0, 0, 0, "", motif_type)
    else:
        # validation des champs saisis dans le formulaire
        errors, nb_side, nb_repet, init_size, rotation_angle, color, _ = validate_inputs(request.form)

        if errors:
            # en cas d'erreurs, on réaffiche la page avec les messages
            return render_template('main.html', errors=errors)

        # génération classique si pas d'erreur
        menu_generate(nb_side, nb_repet, init_size, rotation_angle, color, motif_type)

    # on vérifie si l'image générée existe bien
    if os.path.exists('static/shape.png'):
        # ajout d'un timestamp unique pour éviter le cache navigateur
        image_url = f'static/shape.png?t={int(time.time())}'
        return render_template('main.html', image_url=image_url)
    else:
        return render_template('main.html', errors=["Erreur : image non générée."])

def validate_inputs(data):
    
    # Vérifie la validité des champs du formulaire (types, bornes, etc.)
    # Renvoie :
    #     - une liste d'erreurs éventuelles
    #     - et les valeurs converties sous forme de variables prêtes à l'emploi
    
    errors = []

    # initialisation
    sides = depth = angle = size = None
    color = data.get("color", "")
    motif_type = data.get("motif_type", "repetitive")

    try:
        sides = int(data.get("nb_side", -1))
        if sides < 2:
            errors.append("Le nombre de côtés doit être ≥ 2.")
    except ValueError:
        errors.append("Le nombre de côtés doit être un entier.")

    try:
        depth = int(data.get("nb_repet", -1))
        if depth < 1:
            errors.append("La profondeur ou répétition doit être ≥ 1.")
    except ValueError:
        errors.append("La profondeur ou répétition doit être un entier.")

    try:
        size = float(data.get("init_size", -1))
        if size < 1:
            errors.append("La taille initiale doit être ≥ 1.")
    except ValueError:
        errors.append("La taille initiale doit être un nombre.")

    # l'angle ne s'applique qu'aux formes répétitives
    if motif_type == "repetitive":
        try:
            angle = float(data.get("rotation_angle", -1))
            if angle < 0:
                errors.append("L'angle doit être ≥ 0.")
        except ValueError:
            errors.append("L'angle doit être un nombre.")
    else:
        angle = 0

    return errors, sides, depth, size, angle, color, motif_type

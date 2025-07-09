import os
import time
from flask import Flask, render_template, request
from geometry import *  # importe les fonctions de dessin (forme_rep, spirale, tree, etc.)

# Création de l'application Flask
app = Flask(__name__)

@app.route('/')
def main():
    # Route principale (GET)
    # Affiche la page HTML contenant le formulaire
    return render_template('main.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Route appelée lors de la soumission du formulaire
    # Récupère les paramètres et génère le motif en conséquence

    motif_type = request.form.get("motif_type", "repetitive")  # type choisi dans le select

    if motif_type == "random":
        # Si "Aléatoire" est choisi : appelle directement la génération aléatoire
        menu_generate(0, 0, 0, 0, "", motif_type)
    else:
        # Sinon : on récupère les valeurs du formulaire et on les valide
        errors, nb_side, nb_repet, init_size, rotation_angle, color, _ = validate_inputs(request.form)

        if errors:
            # S'il y a des erreurs → on renvoie la page avec les messages d'erreur
            return render_template('main.html', errors=errors)

        # Sinon → on appelle la fonction de génération avec les bons paramètres
        menu_generate(nb_side, nb_repet, init_size, rotation_angle, color, motif_type)

    # Après la génération, on vérifie si l’image PNG a bien été créée
    if os.path.exists('static/shape.png'):
        # Ajout d’un timestamp pour éviter que le navigateur affiche une ancienne image en cache
        image_url = f'static/shape.png?t={int(time.time())}'
        return render_template('main.html', image_url=image_url)
    else:
        return render_template('main.html', errors=["Erreur : image non générée."])

def validate_inputs(data):
    # Fonction de validation des données du formulaire
    # Vérifie la validité des champs saisis, selon le type de motif
    # Renvoie : (erreurs, nb_côtés, nb_répétitions/profondeur, taille, angle, couleur, motif_type)

    errors = []

    # Initialisation
    sides = depth = angle = size = None
    color = data.get("color", "")
    motif_type = data.get("motif_type", "repetitive")

    # Si ce n’est PAS une fractale, on valide le nombre de côtés
    try:
        sides = int(data.get("nb_side", -1))
        if motif_type != "fractale" and sides < 2:
            errors.append("Le nombre de côtés doit être ≥ 2.")
    except ValueError:
        if motif_type != "fractale":
            errors.append("Le nombre de côtés doit être un entier.")

    # Vérifie la profondeur ou le nombre de répétitions
    try:
        depth = int(data.get("nb_repet", -1))
        if depth < 1:
            errors.append("La profondeur ou répétition doit être ≥ 1.")
    except ValueError:
        errors.append("La profondeur ou répétition doit être un entier.")

    # Vérifie la taille initiale
    try:
        size = float(data.get("init_size", -1))
        if size < 1:
            errors.append("La taille initiale doit être ≥ 1.")
    except ValueError:
        errors.append("La taille initiale doit être un nombre.")

    # Vérifie l'angle uniquement si c’est une forme répétitive
    if motif_type == "repetitive":
        try:
            angle = float(data.get("rotation_angle", -1))
            if angle < 0:
                errors.append("L'angle doit être ≥ 0.")
        except ValueError:
            errors.append("L'angle doit être un nombre.")
    else:
        angle = 0  # dans tous les autres cas, l'angle ne sert pas

    # On renvoie toutes les valeurs utiles pour la génération
    return errors, sides, depth, size, angle, color, motif_type

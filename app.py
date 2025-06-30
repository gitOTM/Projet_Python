import os
import time
import random
from flask import Flask, render_template, request
from geometry import *

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/submit', methods=['POST'])
def submit():
    motif_type = request.form.get("motif_type", "repetitive")

    if motif_type == "random":
        motif_random()

    else:
        errors, nb_side, nb_repet, init_size, rotation_angle, color, _ = validate_inputs(request.form)

        if errors:
            return render_template('main.html', errors=errors)

        # Génère le motif uniquement si tout est valide
        menu_generate(nb_side, nb_repet, init_size, rotation_angle, color, motif_type)

    if os.path.exists('static/shape.png'):
        image_url = f'static/shape.png?t={int(time.time())}'
        return render_template('main.html', image_url=image_url)
    else:
        return render_template('main.html', errors=["Erreur : image non générée."])


def validate_inputs(data):
    errors = []

    # Initialisation par défaut
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

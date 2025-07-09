from PIL import Image
import tkinter as tk
from turtle import RawTurtle, ScrolledCanvas
import math

def menu_generate(
    nb_side: int,
    nb_repet: int,
    init_size: int,
    rotation_angle: int,
    color: str,
    motif_type="repetitive"
):
    # Fonction principale de génération de motif.
    # En fonction du type demandé, elle appelle la fonction de dessin appropriée :
    # - "spiral"   → spirale()
    # - "fractale" → tree()
    # - "random"   → motif_random()
    # - sinon      → forme répétitive

    if motif_type == "spiral":
        return spirale(nb_side, nb_repet, init_size, color)
    elif motif_type == "fractale":
        return tree(nb_repet, init_size, color)
    elif motif_type == "random":
        return motif_random()
    else:
        return forme_rep(nb_side, nb_repet, init_size, rotation_angle, color)


def prepare_turtle(color: str):
    # Prépare une fenêtre invisible avec un canvas et une tortue Turtle prête à dessiner.
    # Configure la couleur, la vitesse, et désactive le rafraîchissement automatique.
    # Retourne : la fenêtre root, le canvas et la tortue t.

    root = tk.Tk()
    root.overrideredirect(True)  # rend la fenêtre invisible à l’utilisateur
    canvas = ScrolledCanvas(root)
    canvas.config(width=600, height=600)
    canvas.pack()

    t = RawTurtle(canvas)
    t.hideturtle()  # ne pas afficher l’icône tortue
    t.speed(0)       # vitesse maximale
    t.color(color)   # applique la couleur
    t.screen.tracer(0, 0)  # désactive le rendu automatique

    return root, canvas, t


def finalize_drawing(t, canvas, root):
    # Termine le dessin :
    # - met à jour l’affichage
    # - exporte le dessin en .eps (format vectoriel)
    # - convertit en .png pour affichage web
    # - ferme la fenêtre tkinter

    t.screen.update()  # mise à jour manuelle de Turtle
    canvas.update()    # mise à jour du canvas tkinter
    canvas.postscript(file="static/shape.eps")  # export EPS
    t.clear()          # nettoie le dessin (facultatif)
    root.destroy()     # ferme proprement la fenêtre
    Image.open("static/shape.eps").save("static/shape.png")  # conversion en PNG


def forme_rep(
    nb_side: int,
    nb_repet: int,
    init_size: int,
    rotation_angle: int,
    color: str
):
    # Génère un motif de forme répétitive :
    # - Trace un polygone à nb_side côtés
    # - Le fait tourner d’un angle à chaque répétition
    # - Crée un effet de rosace ou mandala

    print("Début fonction forme_rep")
    root, canvas, t = prepare_turtle(color)

    # Place la tortue légèrement en bas du centre
    t.penup()
    t.goto(0, -init_size / 2)
    t.setheading(0)
    t.pendown()

    for _ in range(nb_repet):
        for _ in range(nb_side):
            t.forward(init_size)
            t.left(360 / nb_side)
        t.left(rotation_angle)

    finalize_drawing(t, canvas, root)
    print("Fin fonction forme_rep")


def spirale(
    nb_side: int,
    profondeur: int,
    init_size: int,
    color: str
):
    # Génère un motif en spirale :
    # - Chaque itération trace un polygone
    # - La taille augmente à chaque tour (×1.1)
    # - Une rotation progressive crée l’effet spirale

    print("Début fonction spirale")
    root, canvas, t = prepare_turtle(color)

    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    t.pendown()

    length = init_size
    for i in range(profondeur):
        for _ in range(nb_side):
            t.forward(length)
            t.left(360 / nb_side)
        length *= 1.1
        t.left(5)

    finalize_drawing(t, canvas, root)
    print("Fin fonction spirale")


def tree(profondeur: int, size: int, color: str):
    # Génère une fractale simple de type "arbre binaire récursif"
    # - Chaque branche donne naissance à 2 sous-branches inclinées
    # - Les longueurs diminuent à chaque profondeur

    print("Début fonction fractale (tree)")
    root, canvas, t = prepare_turtle(color)

    def branch(depth, length):
        if depth == 0:
            return
        t.forward(length)
        t.left(30)
        branch(depth - 1, length * 0.7)
        t.right(60)
        branch(depth - 1, length * 0.7)
        t.left(30)
        t.backward(length)

    t.penup()
    t.goto(0, -250)  # base de l’arbre
    t.setheading(90)  # pointe vers le haut
    t.pendown()

    branch(profondeur, size)
    finalize_drawing(t, canvas, root)
    print("Fin fonction fractale (tree)")


def motif_random():
    # Génère un motif avec des paramètres aléatoires :
    # - Choisit un type (forme, spirale, fractale)
    # - Gère les paramètres spécifiques à chacun
    # - Retourne le dessin généré

    import random

    motif_type = random.choices(
        ["repetitive", "spiral", "fractale"],
        weights=[0.5, 0.3, 0.2]
    )[0]

    if motif_type == "fractale":
        profondeur = random.randint(3, 6)
        init_size = random.randint(100, 300)
        color = random.choice(["black", "blue", "green", "red", "purple"])
        print(f"[RANDOM] motif_type=fractale, prof={profondeur}, size={init_size}, color={color}")
        return menu_generate(0, profondeur, init_size, 0, color, motif_type)

    # Forme répétitive ou spirale
    nb_side = random.randint(3, 6)
    nb_repet = random.randint(5, 15)
    init_size = random.uniform(20, 200)
    rotation_angle = random.uniform(1, 90)
    color_theme = random.choice([
        ["black", "white", "gray"],
        ["red", "orange", "yellow"],
        ["green", "lightgreen", "cyan"],
        ["blue", "lightblue", "purple"],
        ["pink", "magenta", "brown"]
    ])
    color = random.choice(color_theme)

    print(f"[RANDOM] motif_type={motif_type}, sides={nb_side}, rep={nb_repet}, size={init_size:.1f}, angle={rotation_angle:.1f}, color={color}")
    return menu_generate(nb_side, nb_repet, init_size, rotation_angle, color, motif_type)

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
    # Oriente vers la bonne fonction en fonction du type de motif demandé :
    # - spiral : appelle la fonction spirale
    # - random : appelle motif_random
    # - repetitive (par défaut) : appelle forme_rep
    
    if motif_type == "spiral":
        return spirale(nb_side, nb_repet, init_size, color)
    elif motif_type == "random":
        return motif_random()
    else:
        return forme_rep(nb_side, nb_repet, init_size, rotation_angle, color)


def prepare_turtle(color: str):
    
    # Prépare un environnement graphique Tkinter + Turtle prêt à dessiner
    # avec la couleur choisie et un canvas 600x600.
    # Retourne la racine Tkinter, le canvas et la tortue RawTurtle.
    
    root = tk.Tk()  # fenêtre Tkinter
    root.overrideredirect(True)  # cache la fenêtre pour l'utilisateur
    canvas = ScrolledCanvas(root) # Crée un canvas défilable (zone de dessin) attaché à la fenêtre Tkinter
    canvas.config(width=600, height=600) # Définit les dimensions du canvas à 600x600 pixels
    canvas.pack() # Ajoute le canvas à la fenêtre pour qu’il s’affiche (même si on ne voit pas la fenêtre)
    t = RawTurtle(canvas)  # crée la tortue
    t.hideturtle() # cache l'icone de la tortue
    t.speed(0)  # vitesse maximale
    t.color(color) # aaplique la couleur
    t.screen.tracer(0, 0)  # désactive l'animation automatique
    return root, canvas, t


def finalize_drawing(t, canvas, root):
    
    # Finalise le tracé :
    # - met à jour le canvas
    # - exporte en EPS
    # - convertit en PNG
    # - détruit la fenêtre Tkinter
    
    t.screen.update() # Rafraîchit manuellement l’écran de la tortue
    canvas.update() # Met à jour le canvas Tkinter
    canvas.postscript(file="static/shape.eps")  # export vectoriel
    t.clear()
    root.destroy()
    # conversion en PNG grâce à Pillow
    Image.open("static/shape.eps").save("static/shape.png")


def forme_rep(
    nb_side: int,
    nb_repet: int,
    init_size: int,
    rotation_angle: int,
    color: str
):
    
    # Génère un motif répétitif basé sur un polygone régulier.
    # Le motif est répété avec une rotation à chaque itération
    # pour créer un effet de rosace/toile.
    
    print("Début fonction forme_rep")
    root, canvas, t = prepare_turtle(color)

    # position de départ légèrement sous le centre
    t.penup()
    t.goto(0, -init_size / 2)
    t.setheading(0)
    t.pendown()

    for _ in range(nb_repet):
        # dessiner le polygone
        for _ in range(nb_side):
            t.forward(init_size)
            t.left(360 / nb_side)
        # rotation du motif
        t.left(rotation_angle)

    finalize_drawing(t, canvas, root)
    print("Fin fonction forme_rep")


def spirale(
    nb_side: int,
    profondeur: int,
    init_size: int,
    color: str
):
    
    # Génère un motif en spirale basé sur un polygone.
    # La taille des côtés augmente progressivement à chaque répétition.
    
    print("Début fonction spirale")
    root, canvas, t = prepare_turtle(color)

    t.penup()
    t.goto(0, 0)
    t.setheading(0)
    t.pendown()

    length = init_size
    for i in range(profondeur):
        # tracer le polygone courant
        for _ in range(nb_side):
            t.forward(length)
            t.left(360 / nb_side)
        # agrandit la taille des côtés pour la spirale
        length *= 1.1
        # légère rotation pour accentuer la spirale
        t.left(5)

    finalize_drawing(t, canvas, root)
    print("Fin fonction spirale")


def motif_random():
    
    # Génère un motif de manière aléatoire :
    # - choisit le type de motif
    # - choisit des paramètres aléatoires
    # - puis appelle menu_generate
    
    import random

    # type de motif avec probabilité
    motif_type = random.choices(
        ["repetitive", "spiral"],
        weights=[0.6, 0.4]
    )[0]

    # nombre de côtés : 60% de chance entre 3–6
    if random.random() < 0.6:
        nb_side = random.randint(3, 6)
    else:
        nb_side = random.randint(7, 12)

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

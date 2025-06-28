from PIL import Image
import tkinter as tk
from turtle import RawTurtle, ScrolledCanvas
import math


def menu_generate(nb_side: int, nb_repet: int, init_size: int, rotation_angle: int, color: str, motif_type="repetitive", fractale_form="tree"):
    if motif_type == "spiral":
        return spirale(nb_side, nb_repet, init_size, color)
    elif motif_type == "fractale":
        if fractale_form == "sierpinski":
            return sierpinski(nb_repet, init_size, color)
        elif fractale_form == "koch":
            return koch(nb_repet, init_size, color)
        else:
            return tree(nb_repet, init_size, color)
    else:
        return forme_rep(nb_side, nb_repet, init_size, rotation_angle, color)


def prepare_turtle(color: str):
    root = tk.Tk() #créer une fenêtre invisible
    root.overrideredirect(True) #rend les bordures et titre invisible pour l'utilisateur
    canvas = ScrolledCanvas(root) #créer un canva défilable
    canvas.config(width=600, height=600) #définie la taille de l'espace dessinable 
    canvas.pack() #relie le canva à la fenêtre tkinter et prend tout l'espace disponible
    t = RawTurtle(canvas) #créer une tortue qui va dessiner sur le canva
    t.hideturtle() #cache l'icone de la tortue
    t.speed(0) # met la vitesse de dessin au maximum
    t.color(color) # modifie la couleur des traits
    t.screen.tracer(0, 0) #désactive le rafraichissement de l'écran
    return root, canvas, t


def finalize_drawing(t, canvas, root):
    t.screen.update() #met à jour le dessin pour que tout apparaisse d'un coup
    canvas.update() #pareil
    canvas.postscript(file="static/shape.eps") #sauvegarde le dessin sous format eps
    t.clear() #nettoie la mémoire du dessin
    root.destroy() # ferme la fenêtre tkinter
    Image.open("static/shape.eps").save("static/shape.png") # sauvegarder le eps en png


def forme_rep(nb_side: int, nb_repet: int, init_size: int, rotation_angle: int, color: str):
    print("Début fonction forme_rep")
    root, canvas, t = prepare_turtle(color)

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


def spirale(nb_side: int, profondeur: int, init_size: int, color: str):
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
        length *= 1.1  # spirale croissante
        t.left(5)      # petit angle en plus pour la torsion

    finalize_drawing(t, canvas, root)
    print("Fin fonction spirale")


def tree(depth: int, size: int, color: str):
    print("Début fonction tree")
    root, canvas, t = prepare_turtle(color)

    def draw_branch(length, level):
        if level == 0:
            return
        t.forward(length)
        t.left(30)
        draw_branch(length * 0.6, level - 1)
        t.right(60)
        draw_branch(length * 0.6, level - 1)
        t.left(30)
        t.backward(length)

    t.penup()
    t.goto(0, -200)
    t.setheading(90)  # vers le haut
    t.pendown()

    draw_branch(size, depth)

    finalize_drawing(t, canvas, root)
    print("Fin fonction tree")

def draw_sierpinski_triangle(t, length, depth):
    print("Début fonction draw_sierpinski_triangle")
    if depth == 0:
        for _ in range(3):
            t.forward(length)
            t.left(120)
    else:
        draw_sierpinski_triangle(t, length/2, depth-1)
        t.forward(length/2)
        draw_sierpinski_triangle(t, length/2, depth-1)
        t.backward(length/2)
        t.left(60)
        t.forward(length/2)
        t.right(60)
        draw_sierpinski_triangle(t, length/2, depth-1)
        t.left(60)
        t.backward(length/2)
        t.right(60)
        print("Fin fonction draw_sierpinski_triangle")

def draw_koch_segment(t, length, depth):
    print("Début fonction draw_kowh_segment")
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        draw_koch_segment(t, length, depth-1)
        t.left(60)
        draw_koch_segment(t, length, depth-1)
        t.right(120)
        draw_koch_segment(t, length, depth-1)
        t.left(60)
        draw_koch_segment(t, length, depth-1)
        print("Fin fonction draw_kowh_segment")

def sierpinski(depth: int, size: int, color: str):
    root, canvas, t = prepare_turtle(color)
    t.penup()
    t.goto(-size/2, -size/3)
    t.pendown()
    draw_sierpinski_triangle(t, size, depth)
    finalize_drawing(t, canvas, root)

def koch(depth: int, size: int, color: str):
    root, canvas, t = prepare_turtle(color)
    t.penup()
    t.goto(-size / 2, 0)
    t.setheading(0)
    t.pendown()
    draw_koch_segment(t, size, depth)
    finalize_drawing(t, canvas, root)


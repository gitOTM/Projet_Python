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
    # Oriente vers la bonne fonction en fonction du type de motif demandé.
    
    if motif_type == "spiral":
        return spirale(nb_side, nb_repet, init_size, color)
    elif motif_type == "fractale":
        return tree(nb_repet, init_size, color)
    elif motif_type == "random":
        return motif_random()
    else:
        return forme_rep(nb_side, nb_repet, init_size, rotation_angle, color)


def prepare_turtle(color: str):
    root = tk.Tk()
    root.overrideredirect(True)
    canvas = ScrolledCanvas(root)
    canvas.config(width=600, height=600)
    canvas.pack()
    t = RawTurtle(canvas)
    t.hideturtle()
    t.speed(0)
    t.color(color)
    t.screen.tracer(0, 0)
    return root, canvas, t


def finalize_drawing(t, canvas, root):
    t.screen.update()
    canvas.update()
    canvas.postscript(file="static/shape.eps")
    t.clear()
    root.destroy()
    Image.open("static/shape.eps").save("static/shape.png")


def forme_rep(
    nb_side: int,
    nb_repet: int,
    init_size: int,
    rotation_angle: int,
    color: str
):
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


def spirale(
    nb_side: int,
    profondeur: int,
    init_size: int,
    color: str
):
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
    t.goto(0, -250)
    t.setheading(90)
    t.pendown()

    branch(profondeur, size)
    finalize_drawing(t, canvas, root)
    print("Fin fonction fractale (tree)")


def motif_random():
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

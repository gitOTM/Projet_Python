from PIL import Image
import tkinter as tk
from turtle import RawTurtle, ScrolledCanvas
import math


def menu_generate(nb_side: int, nb_repet: int, init_size: int, rotation_angle: int, color: str, motif_type="repetitive"):
    if motif_type == "spiral":
        return spirale(nb_side, nb_repet, init_size, color)
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
        length *= 1.1  
        t.left(5)      

    finalize_drawing(t, canvas, root)
    print("Fin fonction spirale")


def motif_random():
    import random
    motif_type = random.choice(["repetitive", "spiral"])
    nb_side = random.randint(3, 8)
    nb_repet = random.randint(5, 20)
    init_size = random.uniform(20, 150)
    rotation_angle = random.uniform(5, 45)
    color = random.choice([
        "black", "white", "red", "green", "blue", "yellow", "orange",
        "purple", "pink", "brown", "cyan", "magenta", "gray", "lightblue", "lightgreen"
    ])
    print(f"[RANDOM] motif_type={motif_type}, sides={nb_side}, rep={nb_repet}, size={init_size}, angle={rotation_angle}, color={color}")
    menu_generate(nb_side, nb_repet, init_size, rotation_angle, color, motif_type)



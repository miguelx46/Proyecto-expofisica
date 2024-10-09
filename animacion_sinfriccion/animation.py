import tkinter as tk
from PIL import ImageTk, Image
import time
import math
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

WIDTH = 750
HEIGHT = 400
g = 9.81
x_velocity = 0
y_velocity = 0
time = 0.0

def mover_parabolico():
    global time   
    time += 0.05
    new_x = 0 + x_velocity * time
    new_y = 0 - (y_velocity * time - 0.5 * g * time ** 2)
    
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    if new_x < canvas_width and new_y < canvas_height:
        canvas.coords(imagen_id, new_x, new_y + 310)
        ventana.after(20, mover_parabolico)
    else:
        if new_y >= canvas_height:
            canvas.coords(imagen_id, new_x, new_y)
            print("Pelota fuera de los límites verticales.")

def rotar_imagen():
    vo_st = vopanel.get()
    limx_st = limxpanel.get()
    theta_st = entrada_angulo.get()
    
    if not theta_st or not limx_st or not vo_st:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return
    
    try:
        global imagen_tk, imagen_id, y_inicial, y_velocity, x_velocity, time
        time = 0
        vo = float(vo_st)
        theta = float(theta_st)
        theta_rad = math.radians(theta)
        x_velocity = vo * math.cos(theta_rad)
        y_velocity = vo * math.sin(theta_rad)
        
        imagen = Image.open("balon.png")
        imagen_rotada = imagen.rotate(theta, expand=True)
        imagen_tk = ImageTk.PhotoImage(imagen_rotada)
        
        canvas.delete("all")
        imagen_id = canvas.create_image(10, 50, anchor="nw", image=imagen_tk)
        print("Imagen creada con éxito.")
        y_inicial = 50
        mover_parabolico()
    
    except ValueError:
        messagebox.showwarning("Advertencia", "Por favor ingresa valores numéricos válidos.")

# Procedimiento para graficar velocidad vs posicion (falta con fricción del aire)
def graficar_VX():
    # Capturar variables en los paneles
    vost = vopanel.get()
    limxst = limxpanel.get()
    thetast = entrada_angulo.get()
    
    # Abrir ventana emergente si no se digitó nada en alguno de los paneles
    if not vost or not limxst or not thetast:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return
    
    vo = float(vost)
    limx = int(limxst)
    theta = float(thetast)
    
    theta = np.radians(theta)
    g = 9.81
    
    # Crear arreglos para almacenar los valores de x y y
    t_total = (2 * vo * np.sin(theta)) / g  # Calcular el tiempo total de vuelo
    t = np.linspace(0, t_total, limx)  # Aquí limx es un entero
    xarray = vo * np.cos(theta) * t
    voy = float(vo * np.sin(theta))
    vx = float(vo * np.cos(theta))
    voyarray = voy - (g * t)
    Velarray = np.sqrt((voyarray)**2 + (vx)**2)
    
    plt.plot(xarray, Velarray)
    plt.title("Velocidad de un proyectil")
    plt.xlabel("Distancia (m)")
    plt.ylabel("Velocidad (m/s)")
    plt.grid(True)
    plt.show()

def graficar_YvsX():
    plt.clf()
    vost = vopanel.get()
    limxst = limxpanel.get()
    thetast = entrada_angulo.get()
    
    if not vost or not limxst or not thetast:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return
    
    vo = float(vost)
    limx = int(limxst)
    theta = float(thetast)
    theta = np.radians(theta)
    
    t_total = (2 * vo * np.sin(theta)) / g
    t = np.linspace(0, t_total, limx)
    xarray = vo * np.cos(theta) * t
    yarray = vo * np.sin(theta) * t - (0.5 * g * t**2)
    
    plt.plot(xarray, yarray)
    plt.title("Trayectoria de un proyectil")
    plt.xlabel("Distancia (m)")
    plt.ylabel("Altura (m)")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def reiniciar_simulacion():
    canvas.delete("all")
    vopanel.delete(0, tk.END)
    entrada_angulo.delete(0, tk.END)
    limxpanel.delete(0, tk.END)
    global time
    time = 0

ventana = tk.Tk()
ventana.title("Animación Parabólica")
ventana.configure(bg="#f0f0f0")

canvas = tk.Canvas(ventana, width=WIDTH, height=HEIGHT, bg="white")
canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Entradas
etiqueta_angulo = tk.Label(ventana, text="Ángulo de inclinación (grados):", bg="#f0f0f0", font=("Arial", 12))
etiqueta_angulo.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entrada_angulo = tk.Entry(ventana, font=("Arial", 12))
entrada_angulo.grid(row=1, column=1, padx=10, pady=10)

volabel = tk.Label(ventana, text="Velocidad inicial (m/s):", bg="#f0f0f0", font=("Arial", 12))
volabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
vopanel = tk.Entry(ventana, font=("Arial", 12))
vopanel.grid(row=2, column=1, padx=10, pady=10)

limxlabel = tk.Label(ventana, text="Cantidad de puntos:", bg="#f0f0f0", font=("Arial", 12))
limxlabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")
limxpanel = tk.Entry(ventana, font=("Arial", 12))
limxpanel.grid(row=3, column=1, padx=10, pady=10)
#cargar imagen
img = Image.open("grafica.png")
img_resized = img.resize((80, 60))  # Ajusta el tamaño según sea necesario
img_tk = ImageTk.PhotoImage(img_resized)
# Cargar la imagen del ícono
icon_img = Image.open("logo_expo.png")
icon_img = ImageTk.PhotoImage(icon_img)

# Asignar la imagen como ícono de la ventana principal
ventana.iconphoto(False, icon_img)

# Crear un Label para mostrar la imagen
img_label = tk.Label(ventana, image=img_tk, bg="#f0f0f0")
img_label.grid(row=2, column=2, padx=10, pady=10)  # Ajustar la posición

# Botones
boton_rotar = tk.Button(ventana, text="Mostrar simulacion", command=rotar_imagen, font=("Arial", 12), bg="#4CAF50", fg="white")
boton_rotar.grid(row=1, column=3, padx=10, pady=10)

btnYvsX = tk.Button(ventana, text="Graficar Y vs X", command=graficar_YvsX, font=("Arial", 12), bg="#2196F3", fg="white")
btnYvsX.grid(row=2, column=3, padx=10, pady=10)

# Nuevo botón para graficar Velocidad vs Distancia
btnVX = tk.Button(ventana, text="Graficar V vs X", command=graficar_VX, font=("Arial", 12), bg="#FFC107", fg="black")
btnVX.grid(row=3, column=3, padx=10, pady=10)

boton_reiniciar = tk.Button(ventana, text="Borrar datos", command=reiniciar_simulacion, font=("Arial", 12), bg="#f44336", fg="white")
boton_reiniciar.grid(row=4, column=3, padx=10, pady=10)

# Centrar ventana
ventana.update_idletasks()
width = ventana.winfo_width()
height = ventana.winfo_height()
x = (ventana.winfo_screenwidth() // 2) - (width // 2)
y = (ventana.winfo_screenheight() // 2) - (height // 2)
ventana.geometry(f'{width}x{height}+{x}+{y}')

ventana.mainloop()

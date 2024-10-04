import tkinter as tk
from PIL import ImageTk, Image
import time
import math
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

WIDTH = 900
HEIGHT = 550

x_velocity = 5
y_velocity = -15
gravity = 0.5

# Función para mover la imagen en una trayectoria parabólica
def mover_parabolico():
    global y_velocity
    coords = canvas.coords(imagen_id)
    
    y_velocity += gravity
    canvas.move(imagen_id, x_velocity, y_velocity)
    
    ventana.after(20, mover_parabolico)

# procedimiento para rotar la imagen y luego animarla
def rotar_imagen():
    vost = vopanel.get()
    limxst = limxpanel.get()
    angulost = entrada_angulo.get()
    # abre ventana emergente si no se digito nada en el angulo
    if not entrada_angulo or not limxpanel or not vopanel:
      messagebox.showwarning("Advertencia", "Todas la casillas deben ser llenadas.")
    try:
        global imagen_tk, imagen_id
        angulo = float(angulost)
        
        imagen = Image.open("cohete.png")
        imagen_rotada = imagen.rotate(angulo, expand=True)
        
        # Convertir la imagen a formato que Tkinter pueda usar
        imagen_tk = ImageTk.PhotoImage(imagen_rotada)
        
        # Dibujar la imagen en el canvas
        canvas.delete("all")  # Limpiar el canvas antes de dibujar
        imagen_id = canvas.create_image(10, 50, anchor="nw", image=imagen_tk)

        mover_parabolico()
        
    except Exception as e:
        etiqueta_mensaje.config(text=f"Error: {e}")

# procedimiento para graficar la trayectoria del movimiento (falta con friccion)
def graficar_YvsX():
 plt.clf()
 vost = vopanel.get()
 limxst = limxpanel.get()
 thetast = entrada_angulo.get()
 
 # abre ventana emergente si no se digito nada en algun panel
 if not vost or not limxst or not thetast:
  messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")

 vo = float(vost)
 limx = int(limxst)
 theta = float(thetast)
 theta = np.radians(theta)

 g = 9.81

 # Crear arreglos para almacenar los valores de x y y
 t_total = (2 * vo * np.sin(theta)) / g  # Calcular el tiempo total de vuelo
 t = np.linspace(0, t_total, limx)

 # Calcular las posiciones en x y y
 xarray = vo * np.cos(theta) * t
 yarray = vo * np.sin(theta) * t - (0.5 * g * t**2)

 # Graficar la trayectoria
 plt.plot(xarray, yarray)
 plt.title("Trayectoria de un proyectil")
 plt.xlabel("Distancia (m)")
 plt.ylabel("Altura (m)")
 plt.grid(True)
 plt.show()

ventana = tk.Tk()
ventana.title("Animación Parabólica")
canvas = tk.Canvas(ventana, width=WIDTH, height=HEIGHT, bg="white")
canvas.grid(row=0, column=0, columnspan=3)

# Entradas
etiqueta_angulo = tk.Label(ventana, text="Introduce el ángulo de rotación:")
etiqueta_angulo.grid(row=1, column=0)
entrada_angulo = tk.Entry(ventana)
entrada_angulo.grid(row=1, column=1)

volabel = tk.Label(ventana, text="Introduce la velocidad inicial (m/s):")
volabel.grid(row=2,column=0)
vopanel = tk.Entry(ventana)
vopanel.grid(row=2, column=1)

limxlabel = tk.Label(ventana, text="Introduce la cantidad de puntos:")
limxlabel.grid(row=3,column=0)
limxpanel = tk.Entry(ventana)
limxpanel.grid(row=3, column=1)

#thetalabel = tk.Label(ventana, text="Introduce el ángulo (en grados):")
#thetalabel.grid(row=4,column=0)
#thetapanel = tk.Entry(ventana)
#thetapanel.grid(row=4, column=1)


# Botón para la rotación y animación
boton_rotar = tk.Button(ventana, text="Rotar y Animar Imagen", command=rotar_imagen)
boton_rotar.grid(row=1, column=2)

# boton para mostrar la grafica
btnYvsX = tk.Button(text = 'Graficar X vs Y',command=graficar_YvsX)
btnYvsX.grid(row=2, column=2)

# Etiqueta para mostrar mensajes de error o éxito
etiqueta_mensaje = tk.Label(ventana, text="")
etiqueta_mensaje.grid(row=2, column=0, columnspan=3)

ventana.mainloop()

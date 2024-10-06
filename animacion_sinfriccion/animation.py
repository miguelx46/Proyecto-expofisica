import tkinter as tk
from PIL import ImageTk, Image
import time
import math
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

WIDTH = 1100
HEIGHT = 729

g = 9.81

x_velocity = 0  # Componente horizontal de la velocidad
y_velocity = 0  # Componente vertical de la velocidad
time = 0.0

def mover_parabolico():
    global time
    
    # Incrementar el tiempo en cada frame (20 ms)
    time += 0.02  # Tiempo en segundos
    
    # Obtener las coordenadas actuales de la imagen
    coords = canvas.coords(imagen_id)
    print(f"Coordenadas actuales: {coords}")  # Depuración
    
    # Ecuación de movimiento para la posición en X y Y
    new_x = 0 + x_velocity * time  # 0 es la posición inicial en X
    new_y = 0 - (y_velocity * time - 0.5 * g * time ** 2)  # Ecuación parabólica en Y
    
    # Obtener los límites del canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    #print(f"Nueva posición: ({new_x}, {new_y})")  # Depuración para ver dónde debería ir la pelota
    
    # Evitar que la pelota salga del canvas por abajo o por los lados
    if new_x < canvas_width and new_y < canvas_height:
        # Mover la imagen en el canvas
        canvas.coords(imagen_id, new_x, new_y)
        
        # Continuar el movimiento después de 20 ms
        ventana.after(20, mover_parabolico)
    else:
        # Si la pelota llega al borde inferior, detener el movimiento
        if new_y >= canvas_height:
            canvas.coords(imagen_id, new_x, canvas_height - 50)  # Ajustar para que no salga del canvas
            print("Pelota fuera de los límites verticales.")  # Depuración

def rotar_imagen():
    vo_st = vopanel.get()
    limx_st = limxpanel.get()
    theta_st = entrada_angulo.get()
    
    # Verificar que todas las entradas tengan un valor
    if not theta_st or not limx_st or not vo_st:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return
    
    try:
        global imagen_tk, imagen_id, y_inicial, y_velocity, x_velocity, time
        
        # Resetear el tiempo a 0 al iniciar el movimiento
        time = 0
        vo = float(vo_st)
        theta = float(theta_st)
        
        # Convertir el ángulo de grados a radianes
        theta_rad = math.radians(theta)
        
        # Calcular las componentes de la velocidad inicial
        x_velocity = vo * math.cos(theta_rad)  # Componente horizontal de la velocidad
        y_velocity = vo * math.sin(theta_rad)  # Componente vertical de la velocidad
        
        # Cargar y rotar la imagen
        imagen = Image.open("balon.png")
        imagen_rotada = imagen.rotate(theta, expand=True)
        
        # Convertir la imagen a formato que Tkinter pueda usar
        imagen_tk = ImageTk.PhotoImage(imagen_rotada)
        
        # Limpiar el canvas antes de dibujar
        canvas.delete("all")
        
        # Dibujar la imagen en el canvas en la posición inicial
        imagen_id = canvas.create_image(10, 50, anchor="nw", image=imagen_tk)
        print("Imagen creada con éxito.")  # Depuración
        
        y_inicial = 50  # Posición inicial en y
        
        # Iniciar el movimiento parabólico
        mover_parabolico()
    
    except ValueError:
        messagebox.showwarning("Advertencia", "Por favor ingresa valores numéricos válidos.")

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

 # Ajustar la escala de los ejes para que sea coherente con el ángulo
 plt.axis('equal')

 # Mostrar la gráfica
 plt.show()

ventana = tk.Tk()
ventana.title("Animación Parabólica")
canvas = tk.Canvas(ventana, width=WIDTH, height=HEIGHT, bg="white")
canvas.grid(row=0, column=0, columnspan=3)

# Entradas
etiqueta_angulo = tk.Label(ventana, text="Introduce el ángulo de inclinación:")
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

ventana.update_idletasks()  # Actualizar las tareas de la ventana
width = ventana.winfo_width()
height = ventana.winfo_height()
x = (ventana.winfo_screenwidth() // 2) - (width // 2)
y = (ventana.winfo_screenheight() // 2) - (height // 2)
ventana.geometry(f'{width}x{height}+{x}+{y}')

ventana.mainloop()

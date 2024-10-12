import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import math
import numpy as np
import matplotlib.pyplot as plt

# Constante de gravedad
g = 9.81

# Variables globales de simulación
x_velocity = 0
y_velocity = 0
time_sim = 0.0
simulation_running = False  # Flag para evitar múltiples simulaciones simultáneas

# Coordenadas del arco (ajusta según tu imagen)
arco_x_min = 628
arco_x_max = 695
arco_y_min = 126
arco_y_max = 328

# Posición inicial de la pelota
x0 = 50
y0 = 350

def mover_parabolico():
    global time_sim, x_velocity, y_velocity, simulation_running
    time_sim += 0.05
    new_x = x_velocity * time_sim
    new_y = y_velocity * time_sim - 0.5 * g * time_sim ** 2

    pos_x = x0 + new_x
    pos_y = y0 - new_y  # Invertir el eje Y para que positivo sea hacia arriba


    # Verificar si la pelota entra en el arco
    if arco_x_min <= pos_x <= arco_x_max and arco_y_min <= pos_y <= arco_y_max:
        messagebox.showinfo("¡Gol!", "¡Lo lograste! La pelota ha entrado en el arco.")
        reiniciar_simulacion()
        return
    elif arco_x_min > pos_x > arco_x_max and arco_y_min > pos_y > arco_y_max:
        messagebox.showinfo("Intentalo de nuevo")
        reiniciar_simulacion()

    # Verificar si la pelota está dentro de los límites del canvas
    if 0 <= pos_x <= canvas.winfo_width() and 0 <= pos_y <= canvas.winfo_height():
        canvas.coords(imagen_id, pos_x, pos_y)
        ventana.after(20, mover_parabolico)
    else:
        print("Pelota fuera de los límites. Reiniciando posición.")
        reiniciar_simulacion()

def iniciar_simulacion():
    global x_velocity, y_velocity, time_sim, simulation_running

    if simulation_running:
        messagebox.showwarning("Simulación en curso", "La simulación ya está en ejecución.")
        return

    vo_st = vopanel.get()
    theta_st = entrada_angulo.get()

    if not theta_st or not vo_st:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return

    try:
        vo = float(vo_st)
        theta = float(theta_st)
    except ValueError:
        messagebox.showwarning("Advertencia", "Por favor ingresa valores numéricos válidos.")
        return

    theta_rad = math.radians(theta)
    x_velocity = vo * math.cos(theta_rad)
    y_velocity = vo * math.sin(theta_rad)

    # Rotar la imagen de la pelota si es necesario
    try:
        imagen = Image.open("balon.png")
        imagen_rotada = imagen.rotate(-theta, expand=True)  # Rotación correcta
        imagen_tk_rotada = ImageTk.PhotoImage(imagen_rotada)
        # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
        canvas.image_rotada = imagen_tk_rotada
        canvas.itemconfig(imagen_id, image=imagen_tk_rotada)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo rotar la imagen de la pelota: {e}")
        return

    # Reiniciar posición y tiempo
    canvas.coords(imagen_id, x0, y0)
    time_sim = 0.0
    simulation_running = True
    mover_parabolico()
    print("Simulación iniciada.")

def reiniciar_simulacion():
    global time_sim, x_velocity, y_velocity, simulation_running
    time_sim = 0
    x_velocity = 0
    y_velocity = 0
    simulation_running = False
    # Reinicia la posición de la pelota
    canvas.coords(imagen_id, x0, y0)
    print("Simulación reiniciada.")
    vopanel.delete(0, tk.END)
    entrada_angulo.delete(0, tk.END)
    limxpanel.delete(0, tk.END)
    global time
    time = 0


def graficar_VX():
    vost = vopanel.get()
    limxst = limxpanel.get()
    thetast = entrada_angulo.get()

    if not vost or not limxst or not thetast:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return

    try:
        vo = float(vost)
        limx = int(limxst)
        theta = float(thetast)
    except ValueError:
        messagebox.showwarning("Advertencia", "Por favor ingresa valores numéricos válidos.")
        return

    theta_rad = math.radians(theta)
    g_const = 9.81

    t_total = (2 * vo * math.sin(theta_rad)) / g_const
    t = np.linspace(0, t_total, limx)
    xarray = vo * math.cos(theta_rad) * t
    voyarray = vo * math.sin(theta_rad) - (g_const * t)
    Velarray = np.sqrt(voyarray**2 + (vo * math.cos(theta_rad))**2)

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

    try:
        vo = float(vost)
        limx = int(limxst)
        theta = float(thetast)
    except ValueError:
        messagebox.showwarning("Advertencia", "Por favor ingresa valores numéricos válidos.")
        return

    theta_rad = math.radians(theta)
    t_total = (2 * vo * math.sin(theta_rad)) / g
    t = np.linspace(0, t_total, limx)
    xarray = vo * math.cos(theta_rad) * t
    yarray = vo * math.sin(theta_rad) * t - (0.5 * g * t**2)

    plt.plot(xarray, yarray)
    plt.title("Trayectoria de un proyectil")
    plt.xlabel("Distancia (m)")
    plt.ylabel("Altura (m)")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def inicializar_pelota():
    global imagen_tk, imagen_id
    try:
        imagen = Image.open("balon.png")
        imagen_tk = ImageTk.PhotoImage(imagen)
        # Coloca la pelota en la posición inicial (x0, y0) con ancla 'center'
        imagen_id = canvas.create_image(x0, y0, anchor="center", image=imagen_tk, tags="pelota")
        # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
        canvas.image_pelota = imagen_tk
        print("Pelota inicializada.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen de la pelota: {e}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Animación Parabólica")
ventana.configure(bg="#f0f0f0")

# Tamaño de la ventana ajustado a 65% de la pantalla de ancho y 85% de alto
screen_width = ventana.winfo_screenwidth()
screen_height = ventana.winfo_screenheight()
ventana.geometry(f"{int(screen_width * 0.65)}x{int(screen_height * 0.85)}")

try:
    fondo = Image.open("grama.png")  # Reemplaza 'fondo.png' con el nombre de tu imagen
    fondo_resized = fondo.resize((int(screen_width * 0.65), int(screen_height * 0.85)), Image.LANCZOS)  # Ajustar el tamaño al canvas
    fondo_tk = ImageTk.PhotoImage(fondo_resized)
    # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
    fondo_label = tk.Label(ventana, image=fondo_tk)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")


# Crear el canvas
canvas = tk.Canvas(ventana, width=900, height=500, bg="white")
canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Cargar imagen de la cancha
try:
    foto = Image.open("cancha8.png")
    foto_resized = foto.resize((910, 510), Image.LANCZOS)
    foto_tk = ImageTk.PhotoImage(foto_resized)
    # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
    canvas.image_cancha = foto_tk
    canvas.create_image(0, 0, anchor="nw", image=foto_tk)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen de la cancha: {e}")

# Inicializa la pelota al inicio
inicializar_pelota()

# Entradas
etiqueta_angulo = tk.Label(ventana, text="Ángulo de inclinación (grados):", font=("Georgia", 12))
etiqueta_angulo.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entrada_angulo = tk.Entry(ventana, font=("Arial", 12), bg="black")  
entrada_angulo.grid(row=1, column=1, padx=10, pady=10)

volabel = tk.Label(ventana, text="Velocidad inicial (m/s):", font=("Georgia", 12))
volabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
vopanel = tk.Entry(ventana, font=("Arial", 12), bg="black") 
vopanel.grid(row=2, column=1, padx=10, pady=10)

limxlabel = tk.Label(ventana, text="Cantidad de puntos:", font=("Georgia", 12))
limxlabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")
limxpanel = tk.Entry(ventana, font=("Arial", 12), bg="black") 
limxpanel.grid(row=3, column=1, padx=10, pady=10)


# Cargar imagen del ícono
try:
    icon_img = Image.open("logo_expo.png")
    icon_img = ImageTk.PhotoImage(icon_img)
    ventana.iconphoto(False, icon_img)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar el ícono de la ventana: {e}")



# Botones
boton_rotar = tk.Button(ventana, text="Mostrar simulación", command=iniciar_simulacion, font=("Arial", 12), bg="#4CAF50", fg="black")
boton_rotar.grid(row=1, column=3, padx=10, pady=10)

btnYvsX = tk.Button(ventana, text="Graficar Y vs X", command=graficar_YvsX, font=("Arial", 12), bg="#2196F3", fg="black")
btnYvsX.grid(row=2, column=3, padx=10, pady=10)

# Nuevo botón para graficar Velocidad vs Distancia
btnVX = tk.Button(ventana, text="Graficar V vs X", command=graficar_VX, font=("Arial", 12), bg="#FFC107", fg="black")
btnVX.grid(row=3, column=3, padx=10, pady=10)

boton_borrar = tk.Button(ventana, text="Borrar datos", command=reiniciar_simulacion, font=("Arial", 12), bg="#f44336", fg="black")
boton_borrar.grid(row=4, column=3, padx=10, pady=10)


ventana.mainloop()

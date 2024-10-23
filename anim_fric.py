import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import math
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

g = 9.81

    # Variables globales de simulación
x_velocity = 0
y_velocity = 0
time_sim = 0.0
simulation_running = False  # Flag para evitar múltiples simulaciones simultáneas
k = 0.01  # Prueba con un coeficiente de fricción menor

    # Coordenadas del arco (ajusta según tu imagen)
arco_x_min = 628
arco_x_max = 695
arco_y_min = 126
arco_y_max = 328
# Posición inicial de la pelota
x0 = 50
y0 = 350

def mover_parabolicofric():
    global time_sim, x_velocity, y_velocity, simulation_running, pos_y
    time_sim += 0.05
    
    if k == 0:
        new_x = x_velocity * time_sim
        new_y = y_velocity * time_sim - 0.5 * g * time_sim**2
    else:
        new_x = (x_velocity / k) * (1 - math.exp(-k * time_sim))
        new_y = (y_velocity / k) * (1 - math.exp(-k * time_sim)) - g * time_sim

    pos_x = x0 + new_x
    pos_y = y0 - new_y
        
    print(f"t: {time_sim}, pos_x: {pos_x}, pos_y: {pos_y}, x_velocity: {x_velocity}, y_velocity: {y_velocity}, k: {k}")

    if arco_x_min <= pos_x <= arco_x_max and arco_y_min <= pos_y <= arco_y_max:
        messagebox.showinfo("¡Gol!", "¡Lo lograste! La pelota ha entrado en el arco.")
        reiniciar_simulacion()
        return

    if 0 <= pos_x <= canvas.winfo_width() and 0 <= pos_y <= canvas.winfo_height():
        canvas.coords(imagen_id, pos_x, pos_y)
        ventana.after(2, mover_parabolicofric)  # Cambia 20 por 10 para una animación más rápida
    else:
        print("Pelota fuera de los límites. Reiniciando posición.")
        reiniciar_simulacion()


def iniciar_simulacion():
    global x_velocity, y_velocity, time_sim, simulation_running, k
    if simulation_running:
        messagebox.showwarning("Simulación en curso", "La simulación ya está en ejecución.")
        return
    vo_st = vopanel.get()
    theta_st = entrada_angulo.get()
    k_st = coelabel.get()
    if not theta_st or not vo_st or not k_st:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return
    try:
        vo = float(vo_st)
        theta = float(theta_st)
        k = float(k_st)
        print(f"Vo: {vo}, Theta: {theta}, K: {k}")  # Verificación

        
    
        if k < 0 or k > 1:
            messagebox.showwarning("Coeficiente inválido", "El coeficiente de fricción debe estar entre 0 y 1.")
            return

        if theta == 0:
            messagebox.showwarning("Ángulo horizontal", "El ángulo de lanzamiento es 0, el proyectil se moverá solo horizontalmente.")
            return
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
    mover_parabolicofric()
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
    coelabel.delete(0, tk.END)
    limxpanel.delete(0, tk.END)
    global time 
    time = 0
    
def graficar_VX():
    vost = vopanel.get()
    limxst = limxpanel.get()
    thetast = entrada_angulo.get()
    k_st = coelabel.get()
    if not vost or not limxst or not thetast or not k_st:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return
    try:
        vo = float(vost)
        limx = int(limxst)
        theta = float(thetast)
        k = float(k_st)
    except ValueError:
        messagebox.showwarning("Advertencia", "Por favor ingresa valores numéricos válidos.")
        return
    theta_rad = math.radians(theta)
    t_total = 15 # Estimación de tiempo total
    t = np.linspace(0, t_total, limx)
    xarray = (vo * math.cos(theta_rad) / k) * (1 - np.exp(-k * t))
    voyarray = (vo * math.sin(theta_rad) + g / k) * np.exp(-k * t) - g / k
    velarray = np.sqrt(voyarray**2 + (vo * math.cos(theta_rad) * np.exp(-k * t))**2)
    xarray = xarray[xarray >= 0]

    plt.plot(xarray, velarray)
    plt.title("Velocidad de un proyectil con fricción")
    plt.xlabel("Distancia (m)")
    plt.ylabel("Velocidad (m/s)")
    plt.grid(True)
    plt.show()


def graficar_YvsX():
    plt.clf()
    vost = vopanel.get()
    limxst = limxpanel.get()
    thetast = entrada_angulo.get()
    k_st = coelabel.get()
    if not vost or not limxst or not thetast or not k_st:
        messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
        return
    try:
        vo = float(vost)
        limx = int(limxst)
        theta = float(thetast)
        k = float(k_st)
    except ValueError:
        messagebox.showwarning("Advertencia", "Por favor ingresa valores numéricos válidos.")
        return
    theta_rad = math.radians(theta)
    t_total = 15  # Estimación de tiempo total
    t = np.linspace(0, t_total, limx)
    xarray = (vo * math.cos(theta_rad) / k) * (1 - np.exp(-k * t))
    yarray = ((vo * math.sin(theta_rad) + g / k) / k) * (1 - np.exp(-k * t)) - (g * t) / k
    xarray = xarray[yarray >= 0]
    yarray = yarray[yarray >= 0]
    
    plt.plot(xarray, yarray)
    plt.title("Trayectoria de un proyectil con fricción")
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
ventana.title("Animación Parabólica con fricción")
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
canvas = tk.Canvas(ventana, width=700, height=400, bg="white")
canvas.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

 # Cargar imagen de la cancha
try:
    foto = Image.open("cancha.png")
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
etiqueta_angulo = tk.Label(ventana, text="Ángulo de inclinación (grados):", font=("Georgia", 12),bg="#2ec948")
etiqueta_angulo.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entrada_angulo = tk.Entry(ventana, font=("Arial", 12), bg="white")  
entrada_angulo.grid(row=1, column=1, padx=10, pady=10)

volabel = tk.Label(ventana, text="Velocidad inicial (m/s):", font=("Georgia", 12),bg="#2ec948")
volabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
vopanel = tk.Entry(ventana, font=("Arial", 12), bg="white") 
vopanel.grid(row=2, column=1, padx=10, pady=10)

coelabel = tk.Label(ventana, text="Coeficiente de fricción:", font=("Georgia", 12),bg="#2ec948")
coelabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")
coelabel = tk.Entry(ventana, font=("Arial", 12), bg="white") 
coelabel.grid(row=3, column=1, padx=10, pady=10)

limxlabel = tk.Label(ventana, text="Cantidad de puntos:", font=("Georgia", 12),bg="#2ec948")
limxlabel.grid(row=4, column=0, padx=10, pady=10, sticky="e")
limxpanel = tk.Entry(ventana, font=("Arial", 12), bg="white") 
limxpanel.grid(row=4, column=1, padx=10, pady=10)

# logo de la ventana
try:
    icon_img = Image.open("logo.png")
    icon_img = ImageTk.PhotoImage(icon_img)
    ventana.iconphoto(False, icon_img)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar el ícono de la ventana: {e}")
    
# Botones

# boton animar
try:
    boton_rotar = Image.open("motion.png")  # Reemplaza con el nombre de tu imagen
    animar_img_resized = boton_rotar.resize((30, 30), Image.LANCZOS)  # Ajustar tamaño si es necesario
    animar_img_tk = ImageTk.PhotoImage(animar_img_resized)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen para el botón: {e}")

boton_rotar = tk.Button(
    ventana, 
    text="Animar Pelota", 
    image=animar_img_tk,  # Añadir imagen al botón
    compound="left",  # Posición de la imagen con respecto al texto
    command=mover_parabolicofric, 
    font=("Arial", 12), 
    bg="#15eb1c", 
    fg="black"
)
boton_rotar.grid(row=1, column=3, padx=10, pady=10)

# boton frafica Y vs X

try:
    btnYvsX = Image.open("parabola_YvsX.png")  # Reemplaza con el nombre de tu imagen
    YX_img_resized = btnYvsX.resize((30, 30), Image.LANCZOS)  # Ajustar tamaño si es necesario
    YX_img_tk = ImageTk.PhotoImage(YX_img_resized)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen para el botón: {e}")

btnYvsX = tk.Button(
    ventana, 
    text="Graficar Y vs X", 
    image=YX_img_tk,  # Añadir imagen al botón
    compound="left",  # Posición de la imagen con respecto al texto
    command=graficar_YvsX, 
    font=("Arial", 12), 
    bg="#166bdb", 
    fg="black"
)

btnYvsX.grid(row=2, column=3, padx=10, pady=10)

# boton grafica V vs X

try:
    btnVvsX = Image.open("parabola_VvsX.png")  # Reemplaza con el nombre de tu imagen
    VX_img_resized = btnVvsX.resize((30, 30), Image.LANCZOS)  # Ajustar tamaño si es necesario
    VX_img_tk = ImageTk.PhotoImage(VX_img_resized)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen para el botón: {e}")

btnVvsX = tk.Button(
    ventana, 
    text="Graficar V vs X", 
    image=VX_img_tk,  # Añadir imagen al botón
    compound="left",  # Posición de la imagen con respecto al texto
    command=graficar_VX, 
    font=("Arial", 12), 
    bg="#dbc416", 
    fg="black"
)

btnVvsX.grid(row=3, column=3, padx=10, pady=10)

#boton reiniciar datos
try:
    borrar_img = Image.open("remove.png")  # Reemplaza con el nombre de tu imagen
    borrar_img_resized = borrar_img.resize((30, 30), Image.LANCZOS)  # Ajustar tamaño si es necesario
    borrar_img_tk = ImageTk.PhotoImage(borrar_img_resized)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen para el botón: {e}")

boton_borrar = tk.Button(
    ventana, 
    text="Borrar datos", 
    image=borrar_img_tk,  # Añadir imagen al botón
    compound="left",  # Posición de la imagen con respecto al texto
    command=reiniciar_simulacion, 
    font=("Arial", 12), 
    bg="#f44336", 
    fg="black"
)

boton_borrar.grid(row=4, column=3, padx=10, pady=10)

#texto logo movimiento 
texto_logo = tk.Label(ventana, text="Simulador Movimiento Parabolico\n Con fricción del aire", font=("Georgia", 20), bg="#488c3b", fg="#a6b3b1")
texto_logo.grid(row=0, column=15, padx=10, pady=10, sticky="e")

ventana.mainloop()
import flet as ft
import numpy as np
import matplotlib.pyplot as plt

def main(page: ft.Page):
    # Configurar el tamaño de la ventana
    page.window_width = 700  # Ancho de la ventana
    page.window_height = 550  # Alto de la ventana
    
    # Función del botón "Graficar"
    def button_clicked(e):
        grafica_YvsX
        page.update()

    # Función para graficar Y vs X (puedes agregar la lógica de la gráfica aquí)
    def grafica_YvsX():
        vost = tb1.value
        limxst = tb2.value
        thetast = tb3.value
        
        vo = float(vost)
        limx = int(limxst)
        theta = float(thetast)
        
        g = 9.81
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
        plt.show()
        

    # Definir los elementos de la interfaz
    t = ft.Text()
    tb1 = ft.TextField(label="Velocidad inicial")
    tb2 = ft.TextField(label="Cantidad de puntos")
    tb3 = ft.TextField(label="Angulo de inclinación")
    btn_graficar = ft.ElevatedButton(text="Graficar", on_click=button_clicked)

    # Agregar elementos a la página
    page.add(tb1, tb2, tb3, btn_graficar, t)

ft.app(main)
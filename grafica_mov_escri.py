import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
# función para graficar el movimiento


def calc_grafica():
 
 # datos solo de prueba!!!
 vo = 20
 limx = 120
 theta = 45
 
 theta = np.radians(theta)
 g = 9.81
 # Crear arreglos para almacenar los valores de x y y
 t_total = (2 * vo * np.sin(theta)) / g  # Calcular el tiempo total de vuelo
 t = np.linspace(0, t_total, limx)

 # Calcular las posiciones en x y y
 xarray = vo * np.cos(theta) * t
 yarray = vo * np.sin(theta) * t - (0.5 * g * t**2)

 # Mostrar los valores de x y y
 print("Valores de x:")
 print(xarray)
 print("Valores de y:")
 print(yarray)

 # Graficar la trayectoria
 plt.plot(xarray, yarray)
 plt.title("Trayectoria de un proyectil")
 plt.xlabel("Distancia (m)")
 plt.ylabel("Altura (m)")
 plt.grid(True)
 plt.show()

root = Tk()
root.title("Simulador movimiento") 
#cajas para igresar los datos
vo = Entry(root)
vo.insert(0, vo)
limx = Entry(root)
limx.insert(0, limx)
theta = Entry(root)
theta.insert(0, theta)
vo.pack()
limx.pack()
theta.pack()

myLabeltitulo = Label(root, text = "Simulador movimiento rectilineo", width=80, height=20)
myButton = Button(root, text = "graficar", command=calc_grafica , pady = 40, padx = 40, fg = "blue")
myButton.pack()

myLabeltitulo.pack()

root.mainloop()
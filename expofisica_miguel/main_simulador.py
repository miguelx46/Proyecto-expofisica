import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from tkinter import *
from PIL import ImageTk, Image # type: ignore
from math import sqrt
from tkinter import messagebox
# procedimiento para graficar la trayectoria del movimiento
def calc_grafica_yvsx():
    
 vost = vopanel.get()
 limxst = limxpanel.get()
 thetast = thetapanel.get()
 cdst = cdpanel.get()
 rhost = rhopanel.get()
 Ast = Alabel.get() 
 mst = mlabel.get()

 # abre ventana emergente si no se digito nada en algun panel
 if not vost or not limxst or not thetast or not cdst or not rhost or not Ast or not mst:
     messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")

 vo = float(vost)
 limx = float(limxst)
 theta = float(thetast)
 cd = float(cdst)
 rho = float(rhost)
 A = float(Ast)
 m = float(mst)

 # Convertir ángulo a radianes
 theta = np.radians(theta)
 g = 9.81  # Aceleración debido a la gravedad (m/s^2)

 # Componentes iniciales de la velocidad
 vx = vo * np.cos(theta)
 vy = vo * np.sin(theta)

 # Parámetros iniciales
 dt = 0.01  # Intervalo de tiempo pequeño para la simulación
 x, y = 0, 0  # Posición inicial de x , y
 xarray = [x]
 yarray = [y]

 # Simulación del movimiento
 for _ in range(limx):
     # Magnitud de la velocidad
     v = np.sqrt(vx**2 + vy**2)

     # Fuerza de arrastre
     Fd = 0.5 * cd * rho * A * v**2

     # Aceleraciones con fricción (dividimos por la masa para obtener la aceleración)
     ax = -Fd * (vx / v) / m
     ay = -g - (Fd * (vy / v) / m)

     # Actualización de la posición y velocidad
     vx += ax * dt
     vy += ay * dt
     x += vx * dt
     y += vy * dt

     # Almacenar los valores de x y y
     if y < 0:  # Si el proyectil cae al suelo, se detiene
          break
     xarray.append(x)
     yarray.append(y)

 # Graficar la trayectoria
 plt.plot(xarray, yarray)
 plt.title("Trayectoria de un proyectil con fricción del aire")
 plt.xlabel("Distancia (m)")
 plt.ylabel("Altura (m)")
 plt.grid(True)
 plt.show()

# Grafica velocidad vs posicion (falta con fricción del aire)
def calc_grafica_Vvsx():
    
    #capturar variables en los paneles
    vost = vopanel.get()
    limxst = limxpanel.get()
    thetast = thetapanel.get()
    

    # abre ventana emergente si no se digito nada en alguno de los paneles
    if not vost or not limxst or not thetast:
     messagebox.showwarning("Advertencia", "Todas las casillas deben ser llenadas.")
     
    vo = float(vost)
    limx = float(limxst)
    theta = float(thetast)
    
    theta = np.radians(theta)
    print(theta)
    g = 9.81
    # Crear arreglos para almacenar los valores de x y y
    t_total = (2 * vo * np.sin(theta)) / g  # Calcular el tiempo total de vuelo
    t = np.linspace(0, t_total, limx)
    xarray = vo * np.cos(theta) * t
    voy = float(vo*np.sin(theta))
    vx = float(vo*np.cos(theta))
    voyarray = voy-(g*t)
    Velarray = np.sqrt((voyarray)**2+(vx)**2)
    plt.plot(xarray, Velarray)
    
    plt.title("Velocidad de un proyectil")
    plt.xlabel("Distancia (m)")
    plt.ylabel("Velocidad (m/s)")
    plt.grid(True)
    plt.show()
    
  
# parametros ventana principal
root = Tk()
root.resizable(True, True)
root.geometry("900x650")
root.title("Simulador movimiento")
# cajas para igresar los datos

volabel = Label(root, text="Velocidad inicial en m/s")
volabel.grid(row=0, column=2)
vopanel = Entry(root)
vopanel.grid(row=0, column=1)

limxlabel = Label(root, text="Cantidad de puntos")
limxlabel.grid(row=1, column=2)
limxpanel = Entry(root)
limxpanel.grid(row=1, column=1)

limxlabel = Label(root, text="Angulo de inclinación en grados")
limxlabel.grid(row=2, column=2)
thetapanel = Entry(root)
thetapanel.grid(row=2, column=1)

cdpanel = Label(root, text="Coeficiente de fricción (entre 0.4 y 1)" )
cdpanel.grid(row=3, column=2)
cdpanel = Entry(root)
cdpanel.grid(row=3, column=1)

rhopanel = Label(root, text="Densidad del aire (en kg/m^3)")
rhopanel.grid(row=4, column=2)
rhopanel = Entry(root)
rhopanel.grid(row=4, column=1)

Alabel = Label(root, text="Area de sección transversal (en m^2)")
Alabel.grid(row=5, column=2)
Alabel = Entry(root)
Alabel.grid(row=5, column=1)

mlabel = Label(root, text ="Masa del protectil (en Kg)" )
mlabel.grid(row=6, column=2)
mlabel = Entry(root)
mlabel.grid(row=6, column=1)

# imagen en boton para graficar (en desarollo)
#imagen_btngraficar = PhotoImage(file='expofisica/btn_graficar.jpg')
#labelbtn_graficar = Label(image=imagen_btngraficar)
myLabeltitulo = Label(root, text="Simulador movimiento rectilineo", width=80, height=20)
botonXY = Button(root, text = 'Graficar XvsY',command=calc_grafica_yvsx, pady=30, padx=40)
botonVX = Button(root, text = 'Graficar VvsX',command=calc_grafica_Vvsx, pady=30, padx=40)
#botones para graficar
botonXY.grid(row=8, column=6) 
botonVX.grid(row=8, column=2)
root.mainloop()

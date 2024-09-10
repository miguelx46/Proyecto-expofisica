import numpy as np
import matplotlib.pyplot as plt

limx = int(input("Digite cuantos puntos se van a calcular: "))
theta = float(input("Digite el ángulo de inclinación (en grados): "))
vo = float(input("Digite la velocidad inicial (en m/s): "))

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

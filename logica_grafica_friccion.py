import numpy as np
import matplotlib.pyplot as plt

# Entrada de datos
vo = float(input("Digite la velocidad inicial (en m/s): "))
limx = int(input("Digite cuantos puntos se van a calcular: "))
theta = float(input("Digite el ángulo de inclinación (en grados): "))
cd = float(input("Digite el coeficiente de arrastre (sin unidades, típico entre 0.4 y 1.0): "))
rho = float(input("Digite la densidad del aire (en kg/m^3, típico 1.225 para aire a nivel del mar): "))
A = float(input("Digite el área de sección transversal del proyectil (en m^2): "))
m = float(input("Digite la masa del proyectil (en kg): "))

# Convertir ángulo a radianes
theta = np.radians(theta)
g = 9.81  # Aceleración debido a la gravedad (m/s^2)

# Componentes iniciales de la velocidad
vx = vo * np.cos(theta)
vy = vo * np.sin(theta)

# Parámetros iniciales
dt = 0.01  # Intervalo de tiempo pequeño para la simulación
x, y = 0, 0  # Posición inicial
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

# Mostrar los valores de x y y
print("Valores de x:")
print(xarray)
print("Valores de y:")
print(yarray)

# Graficar la trayectoria
plt.plot(xarray, yarray)
plt.title("Trayectoria de un proyectil con fricción del aire")
plt.xlabel("Distancia (m)")
plt.ylabel("Altura (m)")
plt.grid(True)
plt.show()
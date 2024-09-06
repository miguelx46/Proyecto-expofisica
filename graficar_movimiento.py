import numpy as np
import matplotlib.pyplot as plt 

print("Digite cuantos puntos se van a calcular")
limx = int(input())
limy = limx
ejex = np.linspace(0, 50, limx)
ejey = np.linspace(0, 50, limy)
print("Digite el ángulo de inclinación")
theta = float(input())
print("Digite la velocidad inicial")
vo = float(input()) 
g = -9.81
# tomando valores de x, y para guardarlos en 2 vectores
xarray = np.array([limx])
yarray = np.array([limy])

for t in range(0, limx):
 y = np.sin(theta)*vo*t + (g*t**2)/2
 x = np.cos(theta)*vo*t   
 xarray [t] = x
 yarray [t] = y

print("valores de y")
for t in range(0, limy):
 print(yarray[t])

print("valores de x")
for t in range(0, limx):
 print(xarray[t]) 
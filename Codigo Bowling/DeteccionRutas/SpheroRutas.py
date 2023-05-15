# -*- coding: utf-8 -*-
"""
Creado en Octubre 2022
@author: Mauricio Gallegos
Versión "3.0"
Descripción: Este programa reconoce los colores verde y rojo, además rastrea el color azul que será el sphero.
Recolectando las coordenadas de los colores, calibra al sphero para poder hacer que el sphero vaya hacia los colores.
"""

### Realizar Matríz de Velocidad, Distancia Tiempo




# Calculas distancia entre coordenadas para sacar el tiempo

#Librerias y dependencias
import cv2
import time
import math
from time import sleep
import numpy as np
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from spherov2.adapter.tcp_adapter import get_tcp_adapter

# Variables Globales

### Configuración de Camara ###
frameWidth = 1280
frameHeight = 720
smallGuy = "SM-830E"


# Inicializa la camara
try:
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        # Si no se pudo abrir la cámara externa
        raise ValueError("No se pudo abrir la cámara externa")  
except Exception as e:
    cap = cv2.VideoCapture(0)   # Abrr cámara interna
else:
    # Si se abrió la camata externa, no es necesario hacer nada
    pass    
finally:
    if not cap.isOpened():
        print("Ninguna camara")
    pass

### Variables de Perspectiva
width, height = 8064, 3465

#arreglos NumPy en flotante 32
pts1 = np.float32([[133, 55], [1120, 112], [97, 478], [1097, 545]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

# Parametros getPerspectiveTransorm
# src Coordinates of quadrangle vertices in the source image.
# dst Coordinates of the corresponding quadrangle vertices in the destination image.
matrix = cv2.getPerspectiveTransform(pts1, pts2)

[[70, 60, 63, 85, 255, 255], [3, 130, 100, 8, 255, 255]]

### Pin Color Data ###
myColors_pins = [[88, 130, 200, 92, 155, 240],  # Green Pin
                # [100, 150, 125, 105, 255, 255],  # Blue pin
                # [85, 75, 165, 125, 230, 255],  # Blue pin
                 [0, 80, 86, 15, 255, 150]]  # orange pin

### Pin Coordinate Array ###
pinCoords = [[0, 0], [0, 0], [0, 0]]

### Sphero Color Data###
myColors_sphero = [[100, 125, 125, 110, 255, 255]]  # test val

### Sphero Coordinate Array ###
roboCoords = [[0, 0]]

### Sphero Inicial Coordinate Array ###
inicialRoboCoords = [[0,0]]




def main():
    print("Connecting to Sphero...", end = " ")

    ### Conectar con Sphero Bolt "SM'830E" ###
    toy = scanner.find_toy(toy_name = smallGuy)

    with SpheroEduAPI(toy) as bolt:
        print("DONE!")
        sleep(2)
        print("Encontrando los Puntos...")
        getPinLocation(25)

if __name__ == "__main__":
    main()
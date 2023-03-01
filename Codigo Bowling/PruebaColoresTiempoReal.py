# -*- coding: utf-8 -*-
"""
Creado en Octubre 2022

@author: Mauricio Gallegos
Versión "1.0"

Descripción: Este programa permite configurar los valores de la capa inferior y superior d e HSV para poder 
visualizar de manera mas grafica cuando se reconoce un color en la mascara.

"""




import cv2
import numpy as np

# Crea una imagen en blanco
img = np.zeros((512,512,3), np.uint8)

# Crea una función de llamada de retorno para el evento de movimiento del ratón
def nothing(x):
    pass

# Crea una ventana para mostrar la imagen y los controles deslizantes
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 600, 100)
cv2.moveWindow('image', 10,10)


# Crea controles deslizantes para H, S, V de la capa menor
cv2.createTrackbar('H_l', 'image', 0, 180, nothing)
cv2.createTrackbar('S_l', 'image', 0, 255, nothing)
cv2.createTrackbar('V_l', 'image', 0, 255, nothing)

# Crea controles deslizantes para H, S, V de la capa mayor
cv2.createTrackbar('H_u', 'image', 0, 180, nothing)
cv2.createTrackbar('S_u', 'image', 0, 255, nothing)
cv2.createTrackbar('V_u', 'image', 0, 255, nothing)

# Posiciona los valores iniciales del S, V en los valores default
cv2.setTrackbarPos("S_l", 'image', 50)
cv2.setTrackbarPos("V_l", 'image', 50)
cv2.setTrackbarPos("S_u", 'image', 255)
cv2.setTrackbarPos("V_l", 'image', 255)


# Inicializa la camara de video externa
cap = cv2.VideoCapture(1)

while True:


    # Obtiene el frame actual
    _, imgh = cap.read()

    #imgh = cv2.resize(imgh, (512, 512))

    # Convertir el frame de imagen BGR(RGB) a HSV
    hsvFrame = cv2.cvtColor(imgh, cv2.COLOR_BGR2HSV)
    
    # Obtiene los valores de H, S, V de los controles deslizantes de la capa inferior
    h_l = cv2.getTrackbarPos('H_l', 'image')
    s_l = cv2.getTrackbarPos('S_l', 'image')
    v_l = cv2.getTrackbarPos('V_l', 'image')

    # Obtiene los valores de H, S, V de los controles deslizantes de la capa superior
    h_u = cv2.getTrackbarPos('H_u', 'image')
    s_u = cv2.getTrackbarPos('S_u', 'image')
    v_u = cv2.getTrackbarPos('V_u', 'image')

    capa_inferior = np.array([h_l, s_l, v_l], np.uint8)
    capa_superior = np.array([h_u, s_u, v_u], np.uint8)
    mask = cv2.inRange(hsvFrame, capa_inferior, capa_superior)
    
    # Imprime los valores de H, S, V inferiores en la consola
    print("Valores capa inferior H:", h_l, "S:", s_l, "V:", v_l)
    # Imprime los valores de H, S, V superiores en la consola
    print("Valores capa superior H:", h_u, "S:", s_u, "V:", v_u)
    
    # Morphological Transform, Dilation para cada color  
    kernal = np.ones((5, 5), "uint8")

    img_mask = cv2.dilate(mask, kernal)
    res_mask = cv2.bitwise_and(imgh, imgh, mask = img_mask)

    cv2.imshow("Output", img_mask)
    cv2.moveWindow('Output', 600, 10)
    imgh = cv2.resize(imgh, (512, 512))

    # Espera a que se presione la tecla "q" para salir
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
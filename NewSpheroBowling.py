
# -*- coding: utf-8 -*-
"""
Creado en Octubre 2022
@author: Mauricio Gallegos
Versión "2.0"
"""


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
# camBrightness = 150
bigname = "SB-AA12"


### Empezar la Captura ###
cap = cv2.VideoCapture(1) # 0 es un ID de una camara externa


### Modificar Parametros de Salida de la Captura ###

# Los parametros utilizados por la función set en este codigo son los siguientes:
# El primer parametro es cv::VideoCaptureProperties
# El primer número es Video Capture Properties
# Con el parametro 3 nos referimos a CAP_PROP_FRAME_WIDTH: "With of the frames in the video stream."
# Con el Parametro 4 nos referimos a CAP_PROP_FRAME_HEIGHT: "Height of the frames in the video stream."
# Con el Parametro 10 nos referimos a CAP_PROP_BRIGHTNESS: "Height of the frames in the video stream."
# El segundo parametro de la función set es el valor en pixeles que vamos a asignar

cap.set(3, frameWidth)      
cap.set(4, frameHeight)     
# cap.set(10, camBrightness) 
bigname = "SB-AA12"
smallname = "SM-830E"


### Variables de Perspectiva
width, height = 8064, 3465

#arreglos NumPy en flotante 32
pts1 = np.float32([[133, 55], [1120, 112], [97, 478], [1097, 545]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

# Parametros getPerspectiveTransorm
# src Coordinates of quadrangle vertices in the source image.
# dst Coordinates of the corresponding quadrangle vertices in the destination image.
matrix = cv2.getPerspectiveTransform(pts1, pts2)



### Pin Color Data ###
myColors_pins = [[40, 50, 50, 90, 255, 255],  # Green Pin
                 [100, 150, 125, 105, 255, 255],  # Blue pin
                # [85, 75, 165, 125, 230, 255],  # Blue pin
                 [3, 100, 100, 15, 255, 255]]  # orange pin

### Pin Coordinate Array ###
pinCoords = [[0, 0], [0, 0], [0, 0]]

### Sphero Color Data###
myColors_sphero = [[75, 0, 255, 179, 255, 255]]  # test val

### Sphero Coordinate Array ###
roboCoords = [[0, 0]]



### Función para encontrar colores ###
# Paso de variables del frame de la captura img
# Arreglo de variables de Colores
# Arreglo coordenadas de la locación del sphero
def findColor(img, myColors, myLocations):
    # Se transforma la imagen de BGR a HSV para que se pueda encontrar los colores
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    pinNum = 0
    for color, points in zip(myColors, myLocations):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)

        # Se pasa la mascara con los colores correspondientes 
        #para encotrar los contornos a la función 
        dems = getContours(mask)

        #print("fc.dems", dems)
        #cv2.circle(imgOut, (dems[0], dems[1]), 3, (255, 0, 255), cv2.FILLED)
        if dems[0] != 0 and dems[1] != 0:
            points[0] = dems[0]
            points[1] = dems[1]
        pinNum += 1
    #cv2.imshow("img", mask)


### Función para encontrar los contornos de los colores ###
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1:
            cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(approx)
            x, y, w, h = cv2.boundingRect(approx)
            #cv2.rectangle(img, (x, y), (w + x, h + y), (0, 255, 0), 2)
            x = x + (w // 2)
            y = y + (h // 2)
        print(x, ",", y, end="\r")
    return x, y, w, h



### Función para encontrar el Pin de la lata mas cercana al Sphero ###
def findNextPin(pinCoords, roboCoords):
    num = 0
    count = 0
    short_dist = 0
    for pin in pinCoords:
        dist = math.sqrt((pin[1] - pin[0])**2 + (roboCoords[0][1] - roboCoords[0][0])**2)
        if short_dist == 0:
            short_dist = dist
            num = count
        elif short_dist <= dist:
            short_dist = dist
            num = count
        count += 1
    return num


### Función para encontrar la locación del Pin al que se va a apuntar)
def getPinLocation(numPull):
    while numPull > 0:
        success, img = cap.read()
        imgResult = img.copy()

        ### Setter la perspectiva de acuerdo a la imagen y a la matrix previamente configurada ###
        imgOut = cv2.warpPerspective(img, matrix, (width, height))
        imgOut = cv2.resize(imgOut, (1344, 577))

        # cv2.imshow("warp", imgOut)
        #findColor(imgOut, myColors_sphero, roboCoords)
        findColor(imgOut, myColors_pins, pinCoords)
        #cv2.imshow("Result", imgOut)
        numPull -= 1


def getSpheroLocation(numPull):
    while numPull > 0:
        success, img = cap.read()
        imgResult = img.copy()
        ### Setting up warp perspective ###
        imgOut = cv2.warpPerspective(img, matrix, (width, height))
        imgOut = cv2.resize(imgOut, (1344, 577))
        # cv2.imshow("warp", imgOut)
        #print(myColors_sphero)
        findColor(imgOut, myColors_sphero, roboCoords)
        #cv2.imshow("Result", imgOut)
        numPull -= 1

def findangle(current,target):

    radians = math.atan2(target[1] - current[1], target[0] - current[0])
    degrees = math.degrees(radians)
    print("DONE!")
    if degrees < 0:
        degrees = 360 + degrees 
    degrees = int(degrees)
    return degrees


def distanciaPuntos(start, target):
    x = math.pow(((target[0])-(start[0])), 2)
    y = math.pow(((start[1])-(target[1])), 2)
    dist = (math.sqrt(x+y))
    return dist


def main():
    print("Connecting to Sphero...", end =" ")

    ### Conectar con Sphero Bolt "SM'830E" ###

    toy = scanner.find_toy(toy_name=bigname)
    
    with SpheroEduAPI(toy) as bolt:  
        print("Hecho!")
        sleep(2)
        # sphero.user_io.set_all_leds_8_bit_mask()
        sleep(1)
        print("Encontrando los Puntos...")
        getPinLocation(25)
        print("")
        print("Hecho!")
        print("Gathering Sphero Points...")
        bolt.set_main_led(Color(r=0, g=0, b=255))        
        getSpheroLocation(25)
        print("")
        print("Hecho!")
        print("Coordinadas de los pins:",pinCoords)
        print("Coordinadas del Sphero:",roboCoords)


        ### Calibrar ###
        angle  = 0
        start = [roboCoords[0][0], roboCoords[0][1]]
        sleep(1)
        bolt.roll(0, 0, 2)
        sleep(.75)
        bolt.stop_roll()
        bolt.roll(0, 20, 1)
        sleep(1)
        bolt.stop_roll()
        sleep(1)
        bolt.roll(0, 0, 2)
        sleep(1.25)
        bolt.stop_roll()
        oldCoords = roboCoords
        print("Recolectando punto del Sphero...")
        getSpheroLocation(25)
        print("")
        print("Hecho!")
        print("Coordenadas Sphero:",roboCoords)
        target = [roboCoords[0][0], roboCoords[0][1]]
        print("Calculando Angulo...", end =" ")
        offset_angle = findangle(start,target)

        print("Angulo: ",offset_angle,"grados")


        dist = distanciaPuntos(start, target)
        dist_cm = dist / 8.75
        t = dist_cm / 50



        ### Primer Pin ###
        start = [roboCoords[0][0], roboCoords[0][1]]
        target = [pinCoords[0][0],pinCoords[0][1]]
        print("Calculando Angulo...", end =" ")
        angle = findangle(start,target)
        angle = angle - offset_angle
        if angle < 0:
            print("Ángulo negativo")
            angle = angle + 360
        sleep(1)
        print("Ángulo:",angle,"grados")

        print("Mandando comando...")
        sleep(.25)
        bolt.roll(angle, 0, 1)
        sleep(.75)
        bolt.stop_roll()
        bolt.roll(angle, 100, 2.5)
        sleep(2.5)
        bolt.stop_roll()
        bolt.roll(angle, 0, .25)
        sleep(.25)

        ### Regresar
        angle = 180
        angle = angle - offset_angle
        if angle < 0:
            print("Es negativo")
            angle = angle + 360
        print("Mandando comando...")
        sleep(.25)
        bolt.roll(angle, 0, 1)
        sleep(.75)
        bolt.stop_roll()
        bolt.roll(angle, 100, 2.5)
        sleep(1)
        bolt.stop_roll()
        bolt.roll(angle, 0, 1)
        sleep(.75)
        bolt.stop_roll()


        ### Second Pin ###
        print("Recolectando puntos del Sphero...")
        getSpheroLocation(25)
        print("")
        print("Hecho!")
        print("Coordenadas Sphero:",roboCoords)
        print("Calculando Angulo...", end =" ")
        start = [roboCoords[0][0], roboCoords[0][1]]
        target = [pinCoords[1][0],pinCoords[1][1]]
        angle = findangle(start,target)
        angle = angle - offset_angle
        if angle < 0:
            print("Es negativo")
            angle = angle + 360
        print("Ángulo:",angle,"grados")

        print("Mandando comando...")
        sleep(.25)
        bolt.roll(angle, 0, 1)
        sleep(.75)
        bolt.stop_roll()
        bolt.roll(angle, 100, 1.25)
        sleep(1.25)
        bolt.stop_roll()
        bolt.roll(angle, 0, 1)
        sleep(.25)
        bolt.stop_roll()

        ### Regreso
        angle = 180
        angle = angle - offset_angle
        if angle < 0:
            print("Es negativo")
            angle = angle + 360
        print("Mandando comando...")
        sleep(.25)
        bolt.roll(angle, 0, 1)
        sleep(.75)
        bolt.stop_roll()
        bolt.roll(angle, 100, 1.25)
        sleep(1)
        bolt.stop_roll()
        bolt.roll(angle, 0, 1)
        sleep(.75)
        bolt.stop_roll()

        ### Tercer Pin ###
        print("Recolectando puntos del Sphero...")
        getSpheroLocation(25)
        print("")
        print("Hecho!")
        print("Coordenadas Sphero:",roboCoords)
        print("Calculando Ángulo...", end =" ")
        start = [roboCoords[0][0], roboCoords[0][1]]
        target = [pinCoords[2][0],pinCoords[2][1]]
        angle = findangle(start,target)
        angle = angle - offset_angle
        if angle < 0:
            print("Es negativo")
            angle = angle + 360
        print("Ángulo:",angle,"grados")

        print("Mandando comando...")
        sleep(.25)
        bolt.roll(angle, 0, 1)
        sleep(.75)
        bolt.stop_roll()
        bolt.roll(angle, 100, 1.5)
        sleep(1.5)
        bolt.stop_roll()
        bolt.roll(angle, 0, 1)
        sleep(1)
        bolt.stop_roll()

        print("Terminado...")




if __name__ == "__main__":
    main()



Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
NewSphero/SpheroBowling.py at main · G-Code52/NewSphero
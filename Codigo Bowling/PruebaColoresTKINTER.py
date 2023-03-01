# -*- coding: utf-8 -*-
"""
Creado en Febrero 2023

@author: Mauricio Gallegos
@Versión "2.0"
Lenguaje: Python3
Descripción: Programa para mover los parametros del HSV y mostrar la mascara de bits
para poder identificar un color dentro del rango de valores HSV en tiempo real

"""
'''
# Bloque de librerias y dependencias
  instalar con pip install las siguientes librerias:
  tk, numpy, opencv_python, Pillow
'''

# Libreria para el entorno visual 
import tkinter as tk 
# Libreria para el uso de matrices y arreglos				
import numpy as np
# Libreria con funciones para vision artificial 
import cv2
# Libreria para el manejo de Imagenes
from PIL import Image, ImageTk

# Crea una ventana Principal
root = tk.Tk()
root.geometry("1200x700")

# Crear el lienzo para mostrar la imagen
canvas = tk.Canvas(root, width = 640, height = 360)
canvas.place(x = 310, y = 10)

# Crear las trackbars para los valores inferior y superior del HSV
h_lower = tk.Scale(root, from_=0, to=180, orient=tk.VERTICAL, label = "H_lower", length = "250")
s_lower = tk.Scale(root, from_=0, to=255, orient=tk.VERTICAL, label = "S_lower", length = "250")
v_lower = tk.Scale(root, from_=0, to=255, orient=tk.VERTICAL, label = "V_lower", length = "250")
h_upper = tk.Scale(root, from_=0, to=180, orient=tk.VERTICAL, label = "H_upper", length = "250")
s_upper = tk.Scale(root, from_=0, to=255, orient=tk.VERTICAL, label = "S_upper", length = "250")
v_upper = tk.Scale(root, from_=0, to=255, orient=tk.VERTICAL, label = "V_upper", length = "250")

# Alinear las trackbars en la ventana
h_lower.place(x = 10, y = 10)
s_lower.place(x = 110, y = 10)
v_lower.place(x = 210, y = 10)
h_upper.place(x = 10, y = 280)
s_upper.place(x = 110, y = 280)
v_upper.place(x = 210, y = 280)

# Inicializa la camara
cap = cv2.VideoCapture(1)

def VideoCapture():
	""" Permite la captura y Procesamiento del frame """

	# Obtiene el frame actual
	ret, img = cap.read()

	# Convertir el frame de imagen BGR(RGB) a HSV
	hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Obtiene los valores ed los rangos inferiores HSV
	h_l = h_lower.get()
	s_l = s_lower.get()
	v_l = v_lower.get()

	# Obtiene los valores ed los rangos superiores HSV
	h_u = h_upper.get()
	s_u = s_upper.get()
	v_u = v_upper.get()

	# Guarda los valores HSV en un arreglo para el inferior y superior
	lower_mask = np.array([h_l, s_l, v_l], np.uint8)
	upper_mask = np.array([h_u, s_u, v_u], np.uint8)
	mask = cv2.inRange(hsvFrame, lower_mask, upper_mask)

	# Imprime los valores de H, S, V inferiores en la consola
	print("Valores capa inferior H:", h_l, "S:", s_l, "V:", v_l)
	# Imprime los valores de H, S, V superiores en la consola
	print("Valores capa superior H:", h_u, "S:", s_u, "V:", v_u)

	# Morphological Transform, Dilation para cada color 
	kernal = np.ones((5, 5), "uint8")

	# Remueve el ruido visual
	img_mask = cv2.dilate(mask, kernal)
	res_mask = cv2.bitwise_and(img, img, mask = img_mask)

	# Convierte la imagen a un arreglo de bits para poder mostrarla en el Canvas
	img_arr = Image.fromarray(res_mask)
	imgtk = ImageTk.PhotoImage(image = img_arr)

	# Agrega el Frame al Canvas
	canvas.imgtk = imgtk
	canvas.create_image(0, 0, anchor = tk.NW, image = imgtk)
	root.after(10, VideoCapture)

# Actualiza la ventana después de 10ms
VideoCapture()

# Inicializa el bucle de eventos principales de la ventana
root.mainloop()


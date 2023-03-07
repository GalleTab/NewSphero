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
import tkinter as tk 
import numpy as np
import cv2
from PIL import Image, ImageTk
import sys

# establece el límite de profundidad de recursión a 10000
sys.setrecursionlimit(10000) # establece el límite de profundidad de recursión a 10000


# Definir variables globales
h_lower = None
s_lower = None
v_lower = None
h_upper = None
s_upper = None
v_upper = None
capturando_video = True

def color_picker():
	# Inicialización de las variables globales
	global h_lower, s_lower, v_lower, h_upper, s_upper, v_upper

	# Creacion y configuración de la ventana principal (root)
	root = tk.Tk()
	root.geometry("1300x700")
	root.configure(background="#19222B")

	# Creación del Widget Canvas para mostrar el video
	canvas = tk.Canvas(root, width = 640, height = 360, background="#86895d")
	canvas.place(x = 500, y = 170)

	# Creación de las trackbars para modificar los valores inferiores y superiores 
	# del rango HSV
	h_lower = tk.Scale(root, from_=0, to=180, 
		orient=tk.VERTICAL, label = "H_lower", 
		length = "250", background="#BD9240", 
		troughcolor = "#DDD6CC")
	s_lower = tk.Scale(root, from_=0, to=255, 
		orient=tk.VERTICAL, label = "S_lower", 
		length = "250", background="#BD9240", 
		troughcolor = "#DDD6CC")
	v_lower = tk.Scale(root, from_=0, to=255, 
		orient=tk.VERTICAL, label = "V_lower", 
		length = "250", background = "#BD9240", 
		troughcolor = "#DDD6CC")
	h_upper = tk.Scale(root, from_=0, to=180, 
		orient=tk.VERTICAL, label = "H_upper", 
		length = "250", background = "#BD9240", 
		troughcolor = "#DDD6CC")
	s_upper = tk.Scale(root, from_=0, to=255, 
		orient=tk.VERTICAL, label = "S_upper", 
		length = "250", background = "#BD9240", 
		troughcolor = "#DDD6CC")
	v_upper = tk.Scale(root, from_=0, to=255, 
		orient=tk.VERTICAL, label = "V_upper", 
		length = "250", background = "#BD9240", 
		troughcolor = "#DDD6CC")
	
	# Se posicionan las trackbars en la ventana principal
	h_lower.place(x = 50, y = 50)
	s_lower.place(x = 170, y = 50)
	v_lower.place(x = 290, y = 50)
	h_upper.place(x = 50, y = 400)
	s_upper.place(x = 170, y = 400)
	v_upper.place(x = 290, y = 400)

	# Inicializa la camara externa, si no se encuentra, inicializa la camara default
	try:
		cap = cv2.VideoCapture(1)
		if not cap.isOpened():
			raise ValueError("No se pudo abrir la cámara externa")  
	except Exception as e:
		cap = cv2.VideoCapture(0) 
	else:
		pass	
	finally:
		if not cap.isOpened():
			print("Ninguna camara")

	VideoCapture(cap, root, canvas)

def VideoCapture(cap, root, canvas):
	# Permite la captura y Procesamiento del frame

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
	root.after(100, VideoCapture, cap, root, canvas)

	# Inicializa el bucle de eventos principales de la ventana
	root.mainloop()

color_picker()
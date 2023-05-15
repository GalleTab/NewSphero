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
from tkinter import ttk
# Libreria para el uso de matrices y arreglos				
import numpy as np
# Libreria con funciones para vision artificial 
import cv2
# Libreria para el manejo de Imagenes
from PIL import Image, ImageTk

from djitellopy import tello

import time


'''
# Funiones de los botones

'''

# Arreglo de Colores
myColors_pins = [[0, 0, 0, 0, 0, 0],  # Green Pin
                # [100, 150, 125, 105, 255, 255],  # Blue pin
                # [85, 75, 165, 125, 230, 255],  # Blue pin
                 [0, 0, 0, 0, 0, 0]]  # orange pin


def close():
	# Cierra el programa al presionar el boton

	print("Cerrando el Programa")

	# Termina los procesos de la ventana root
	root.destroy()
	root.quit()


def getValoresVerde():
	# Recolecta los valores inferiores y superiores del rango HSV

	# Rangos inferiores
	myColors_pins[0][0] = h_lower.get()
	myColors_pins[0][1] = s_lower.get()
	myColors_pins[0][2] = v_lower.get()

	# Rangos superiores
	myColors_pins[0][3] = h_upper.get()
	myColors_pins[0][4] = s_upper.get()
	myColors_pins[0][5] = v_upper.get()	

	print("Valores HSV Verde Recogidos")


def getValoresRojo():
	# Recolecta los valores inferiores y superiores del rango HSV

	# Rangos inferiores
	myColors_pins[1][0] = h_lower.get()
	myColors_pins[1][1] = s_lower.get()
	myColors_pins[1][2] = v_lower.get()

	# Rangos superiores
	myColors_pins[1][3] = h_upper.get()
	myColors_pins[1][4] = s_upper.get()
	myColors_pins[1][5] = v_upper.get()

	print("Valores HSV Rojo Recogidos")


def PrintArray():
	print(myColors_pins)


'''
def subir_H_inferior():
	range = h_lower.get()
	h_lower.set(range - 1)

def bajar_H_inferior():
	range = h_lower.get()
	h_lower.set(range + 1)

def subir_S_inferior():
	range = s_lower.get()
	s_lower.set(range - 1)

def bajar_S_inferior():
	range = s_lower.get()
	s_lower.set(range + 1)

def subir_V_inferior():
	range = v_lower.get()
	v_lower.set(range - 1)

def bajar_V_inferior():
	range = v_lower.get()
	v_lower.set(range + 1)

def pressed_button():
'''
def adjust_value(button_id, adjustment):
    if button_id == "subir_hinf":
        range = h_lower.get()
        h_lower.set(range + adjustment)
    elif button_id == "bajar_hinf":
        range = h_lower.get()
        h_lower.set(range + adjustment)
    elif button_id == "subir_sinf":
        range = s_lower.get()
        s_lower.set(range + adjustment)
    elif button_id == "bajar_sinf":
        range = s_lower.get()
        s_lower.set(range + adjustment)
    elif button_id == "subir_vinf":
        range = v_lower.get()
        v_lower.set(range + adjustment)
    elif button_id == "bajar_vinf":
        range = v_lower.get()
        v_lower.set(range + adjustment)
    elif button_id == "subir_hsup":
        range = h_upper.get()
        h_upper.set(range + adjustment)
    elif button_id == "bajar_hsup":
        range = h_upper.get()
        h_upper.set(range + adjustment)
    elif button_id == "subir_ssup":
        range = s_upper.get()
        s_upper.set(range + adjustment)
    elif button_id == "bajar_ssup":
        range = s_upper.get()
        s_upper.set(range + adjustment)
    elif button_id == "subir_vsup":
        range = v_upper.get()
        v_upper.set(range + adjustment)
    elif button_id == "bajar_vsup":
        range = v_upper.get()
        v_upper.set(range + adjustment)



# Crea una ventana Principal
root = tk.Tk()
root.geometry("1300x700")
root.configure(background="#19222B")

# Crear el lienzo para mostrar la imagen
canvas = tk.Canvas(root, width = 640, height = 360, background="#86895d")
canvas.place(x = 500, y = 170)

# Crear las trackbars para los valores inferior y superior del HSV
h_lower = tk.Scale(root, from_=0, 
	to=180, orient=tk.VERTICAL, 
		label = "H_lower", 
	length = "250",
	background="#BD9240",
	troughcolor = "#DDD6CC"
	)
s_lower = tk.Scale(root, from_=0,
 	to=255, orient=tk.VERTICAL,
 	label = "S_lower",
 	length = "250",
 	background="#BD9240",
	troughcolor = "#DDD6CC"
 	)
v_lower = tk.Scale(root, from_=0, 
	to=255, orient=tk.VERTICAL, 
	label = "V_lower",
	length = "250", 
	background = "#BD9240",
	troughcolor = "#DDD6CC"
	)
h_upper = tk.Scale(root, from_=0, 
	to=180, orient=tk.VERTICAL, 
	label = "H_upper", 
	length = "250",
	background = "#BD9240",
	troughcolor = "#DDD6CC"
	)
s_upper = tk.Scale(root, from_=0, to=255, 
	orient=tk.VERTICAL, 
	label = "S_upper", 
	length = "250", 
	background = "#BD9240",
	troughcolor = "#DDD6CC"
	)
v_upper = tk.Scale(root, from_=0, to=255, 
	orient=tk.VERTICAL, 
	label = "V_upper", 
	length = "250", 
	background = "#BD9240",
	troughcolor = "#DDD6CC"
	)

# Alinear las trackbars en la ventana
h_lower.place(x = 50, y = 50)
s_lower.place(x = 170, y = 50)
s_lower.set(100)
v_lower.place(x = 290, y = 50)
v_lower.set(100)
h_upper.place(x = 50, y = 400)
h_upper.set(180)
s_upper.place(x = 170, y = 400)
s_upper.set(255)
v_upper.place(x = 290, y = 400)
v_upper.set(255)

### Botones 


# Crear el objeto Style y asignarle un nombre
estilo = ttk.Style()
estilo.configure("My.TButton", foreground="#BD9240", background="#BD9240", font=("Verdana", 12))

# Boton Cerrar el Programa
btn_cerrar = ttk.Button(text="Cerrar", command=close, style="My.TButton")
btn_cerrar.place(x=500, y=600)

# Boton Recolectar datos HSV Rojo
btn_HSV_rojo = ttk.Button(text="HSV Rojo", command=getValoresRojo, style="My.TButton")
btn_HSV_rojo.place(x=685, y=600)

# Boton Recolectar datos HSV Verde
btn_HSV_verde = ttk.Button(text="HSV Verde", command=getValoresVerde, style="My.TButton")
btn_HSV_verde.place(x=870, y=600)

# Imprimir los valores
btn_print = ttk.Button(text="Imprimir", command=PrintArray, style="My.TButton")
btn_print.place(x=1055, y=600)

# Botones bajar rango
'''
btn_subir_hinf = ttk.Button(text="∧", command=subir_H_inferior, style="My.TButton", width = "2")
btn_subir_hinf.place(x=100, y=250)
btn_bajar_hinf = ttk.Button(text="∨", command=bajar_H_inferior, style="My.TButton", width = "2")
btn_bajar_hinf.place(x=100, y=275)

btn_subir_sinf = ttk.Button(text="∧", command=subir_S_inferior, style="My.TButton", width = "2")
btn_subir_sinf.place(x=220, y=250)
btn_bajar_sinf = ttk.Button(text="∨", command=bajar_S_inferior, style="My.TButton", width = "2")
btn_bajar_sinf.place(x=220, y=275)

btn_subir_vinf = ttk.Button(text="∧", command=subir_V_inferior, style="My.TButton", width = "2")
btn_subir_vinf.place(x=340, y=250)
btn_bajar_vinf = ttk.Button(text="∨", command=bajar_V_inferior, style="My.TButton", width = "2")
btn_bajar_vinf.place(x=340, y=275)

btn_subir_hsup = ttk.Button(text="∧", command=subir_H_inferior, style="My.TButton", width = "2")
btn_subir_hsup.place(x=100, y=250)
btn_bajar_hsup = ttk.Button(text="∨", command=bajar_H_inferior, style="My.TButton", width = "2")
btn_bajar_hsup.place(x=100, y=275)

btn_subir_ssup = ttk.Button(text="∧", command=subir_S_inferior, style="My.TButton", width = "2")
btn_subir_ssup.place(x=220, y=250)
btn_bajar_ssup = ttk.Button(text="∨", command=bajar_S_inferior, style="My.TButton", width = "2")
btn_bajar_ssup.place(x=220, y=275)

btn_subir_vsup = ttk.Button(text="∧", command=subir_V_inferior, style="My.TButton", width = "2")
btn_subir_vsup.place(x=340, y=250)
btn_bajar_vsup = ttk.Button(text="∨", command=bajar_V_inferior, style="My.TButton", width = "2")
btn_bajar_vsup.place(x=340, y=275)
'''
btn_subir_hinf = ttk.Button(text="∧", command=lambda: adjust_value("subir_hinf", -1), style="My.TButton", width = "2")
btn_subir_hinf.place(x=100, y=250)
btn_bajar_hinf = ttk.Button(text="∨", command=lambda: adjust_value("bajar_hinf", 1), style="My.TButton", width = "2")
btn_bajar_hinf.place(x=100, y=275)

btn_subir_sinf = ttk.Button(text="∧", command=lambda: adjust_value("subir_sinf", -1), style="My.TButton", width = "2")
btn_subir_sinf.place(x=220, y=250)
btn_bajar_sinf = ttk.Button(text="∨", command=lambda: adjust_value("bajar_sinf", 1), style="My.TButton", width = "2")
btn_bajar_sinf.place(x=220, y=275)

btn_subir_vinf = ttk.Button(text="∧", command=lambda: adjust_value("subir_vinf", -1), style="My.TButton", width = "2")
btn_subir_vinf.place(x=340, y=250)
btn_bajar_vinf = ttk.Button(text="∨", command=lambda: adjust_value("bajar_vinf", 1), style="My.TButton", width = "2")
btn_bajar_vinf.place(x=340, y=275)

btn_subir_hsup = ttk.Button(text="∧", command=lambda: adjust_value("subir_hsup", -1), style="My.TButton", width = "2")
btn_subir_hsup.place(x=100, y=600)
btn_bajar_hsup = ttk.Button(text="∨", command=lambda: adjust_value("bajar_hsup", 1), style="My.TButton", width = "2")
btn_bajar_hsup.place(x=100, y=625)

btn_subir_ssup = ttk.Button(text="∧", command=lambda: adjust_value("subir_ssup", -1), style="My.TButton", width = "2")
btn_subir_ssup.place(x=220, y=600)
btn_bajar_ssup = ttk.Button(text="∨", command=lambda: adjust_value("bajar_ssup", 1), style="My.TButton", width = "2")
btn_bajar_ssup.place(x=220, y=625)

btn_subir_vsup = ttk.Button(text="∧", command=lambda: adjust_value("subir_vsup", -1), style="My.TButton", width = "2")
btn_subir_vsup.place(x=340, y=600)
btn_bajar_vsup = ttk.Button(text="∨", command=lambda: adjust_value("bajar_vsup", 1), style="My.TButton", width = "2")
btn_bajar_vsup.place(x=340, y=625)


# Inicializa la camara
###
#inicializar el drone como "me"
me = tello.Tello()
#conectar el drone, es importante dejar el False para ignorar paquetes de estado
me.connect(False)
time.sleep(1)
me.streamon()
	

def VideoCapture():
	""" Permite la captura y Procesamiento del frame """
	cap = cv2.VideoCapture(0)
	_, img = cap.read()
        

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
	# print("Valores capa inferior H:", h_l, "S:", s_l, "V:", v_l)
	# Imprime los valores de H, S, V superiores en la consola
	# print("Valores capa superior H:", h_u, "S:", s_u, "V:", v_u)

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


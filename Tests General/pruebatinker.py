import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk

# Crea una ventana principal
root = tk.Tk()
root.geometry("300x200")

# Crea un lienzo para mostrar la imagen
canvas = tk.Canvas(root, width=256, height=256)
canvas.pack()

# Crea controles deslizantes para H, S, V
h_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="H")
s_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="S")
v_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="V")
h_scale.pack()
s_scale.pack()
v_scale.pack()

def update_image():
    # Obtiene los valores de H, S, V de los controles deslizantes
    h = h_scale.get()
    s = s_scale.get()
    v = v_scale.get()
    
    # Actualiza el lienzo con la imagen HSV
    hsv_image = np.zeros((256, 256, 3), dtype=np.uint8)
    hsv_image[:,:,0] = h
    hsv_image[:,:,1] = s
    hsv_image[:,:,2] = v
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    img = Image.fromarray(bgr_image)
    imgtk = ImageTk.PhotoImage(image=img)
    canvas.imgtk = imgtk
    canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
    
    # Actualiza la ventana después de 10ms
    root.after(10, update_image)

# Llama a la función de actualización de imagen
update_image()

# Inicia el bucle de eventos principal de la ventana
root.mainloop()

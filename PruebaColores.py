
import cv2
import time
import numpy as np

def ColorTracking():
    cap = cv2.VideoCapture(0) #inicializar camara computadora
    centers = np.empty #Crear matriz para 
    while True:

        #primer argumento es un valor booleano, devuelve True si el marco de lectura es correcto y si el archivo se lee hasta el final, su valor de retorno es False.
        #obtener el frame actual
        _, img = cap.read()

        #cambiar dimensiones de la imagen
        img = cv2.resize(img, (1000, 850))

        #Covertir el frame de imagen en BGR(RGB) a HSV(hue-saturaton-value)
        hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Rango para el color rojo
        red_l = np.array([170, 120, 120], np.uint8)
        red_u = np.array([180, 255, 255], np.uint8)
        red_m = cv2.inRange(hsvFrame, red_l, red_u)

        # Rango para el color verde
        green_l = np.array([40, 100, 50], np.uint8)
        green_u = np.array([90, 255, 255], np.uint8)
        green_m = cv2.inRange(hsvFrame, green_l, green_u)

        # Rango para el color azul
        blue_l = np.array([100, 150, 125], np.uint8)
        blue_u = np.array([110, 255, 255], np.uint8)
        blue_m = cv2.inRange(hsvFrame, blue_l, blue_u)

 
        # Morphological Transform, Dilation para cada color 
        kernal = np.ones((5, 5), "uint8")

        # Para el color rojo
        red_m = cv2.dilate(red_m, kernal)
        res_red = cv2.bitwise_and(img, img, mask = red_m)

        # Para el color verde
        green_m = cv2.dilate(green_m, kernal)
        res_green = cv2.bitwise_and(img, img, mask = green_m)

        # Para el color azul
        blue_m = cv2.dilate(blue_m, kernal)
        res_blue = cv2.bitwise_and(img, img, mask = blue_m)


        # Crear contorno para trackear el color rojo
        cont, hierarchy = cv2.findContours(red_m, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE)

        for pic, cont in enumerate(cont):
            area = cv2.contourArea(cont)
            if(area > 300):
                x, y, w, h =cv2.boundingRect(cont)
                img = cv2.rectangle(img, (x, y), 
                                    (x + w, y + h),
                                    (0, 0, 255), 2)


                cv2.putText(img, "Color Rojo", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))

                

        # Crear contorno para trackear el color verde
        cont, hierarchy = cv2.findContours(green_m,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, cont in enumerate(cont):
            area = cv2.contourArea(cont)
            if(area > 300):
                x, y, w, h =cv2.boundingRect(cont)
                img = cv2.rectangle(img, (x, y), 
                                    (x + w, y + h),
                                    (0, 255, 0), 2)

                
                cv2.putText(img, "Color Verde", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))

        # Crear contorno para trackear el color azul
        cont, hierarchy = cv2.findContours(blue_m,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        for pic, cont in enumerate(cont):
            area = cv2.contourArea(cont)
            if(area > 300):
                x, y, w, h =cv2.boundingRect(cont)
                img = cv2.rectangle(img, (x, y), 
                                    (x + w, y + h),
                                    (255, 0, 0), 2)

                cv2.putText(img, "Color Azul", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))
                




        cv2.imshow("Output", img)
        cv2.imshow("Mask", red_m)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break



#def PathTracking():




# Codigo
ColorTracking()

#Librerias y dependencias

from time import sleep
import numpy as np
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from spherov2.adapter.tcp_adapter import get_tcp_adapter
from pynput import keyboard as kb



bigname = "SB-AA12"
smallname = "SM-830E"

def pulsa(tecla):
	if tecla == kb.KeyCode.from_char('a'):
		h = bolt.get_heading()
		bolt.set_heading(h-10)
		print('Se ha soltado la tecla ' + str(tecla))
		bolt.reset_aim()
		pass
	if tecla == kb.KeyCode.from_char('d'):
		h = bolt.get_heading()
		bolt.set_heading(h+10)
		print('Se ha soltado la tecla ' + str(tecla))
		bolt.reset_aim()
		pass
	if tecla == kb.KeyCode.from_char('q'):
		print('Se ha soltado la tecla ' + str(tecla))
		return False
		pass



def calibrarDireccion(bolt):
    print("Calibrando Luz Trasera")
    bolt.reset_aim()
    bolt.set_main_led(Color(r=0, g=0, b=0))
    bolt.set_back_led(0)  # Dim
    sleep(2)
    bolt.set_back_led(255)  # Bright
    sleep(2)
    kb.Listener(pulsa).run()



toy = scanner.find_toy(toy_name=smallname)


with SpheroEduAPI(toy) as bolt:  
        print("Hecho!")

        bolt.set_main_led(Color(r=0, g=0, b=255)) 
        calibrarDireccion(bolt)
        bolt.roll(0, 15, 1)
        sleep(2)
        bolt.roll(90 ,15, 1)
        sleep(2)
        bolt.roll(0, 15, 1)


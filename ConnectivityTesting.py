#Librerias y dependencias

import time
import numpy as np
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from spherov2.adapter.tcp_adapter import get_tcp_adapter


bigname = "SB-AA12"


toy = scanner.find_toy(toy_name=bigname)

with SpheroEduAPI(toy) as bolt:  
        print("Hecho!")

        bolt.set_main_led(Color(r=0, g=0, b=255)) 
        bolt.roll(0, 0, 2)

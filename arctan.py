import time
import math

radians = math.atan2(186 - 209, 1342 - 1243)
print("angulo en radianes",radians)
degrees = math.degrees(radians)
print("HECHO!")
#if degrees < 0:
#	degrees = 360 + degrees
degrees = int(degrees)
print("angulo radianes trunc",degrees)

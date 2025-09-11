import nanovna as vna
import math
import matplotlib.pyplot as plot


freq_init = 50e3
freq_final = 6e9
points_measure = 1000
mpp = 5 #measure per points 


device = vna.Nvna(3,baudrate=2e6)#Teste com VNA de verdade

device.detect()
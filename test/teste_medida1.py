import nanovna as vna
import math
import matplotlib.pyplot as plot
from driver_lib import positioner


freq_init = 50e3
freq_final = 6e9
points_measure = 1000
mpp = 5 #measure per points 


pos = positioner()
pos.connect()

device = vna.Nvna(3,baudrate=2e6)#Teste com VNA de verdade

device.calibration(freq_init,#Frequência inicial
        freq_final, #frequência final
        points_measure,#Nº de pontos
        mpp)

input("Calibração finalizada!")

for nm in range(10):
    device.measure(freq_init,freq_final,points_measure,mpp)
    device.calibrate_S11()

    f, real,imag = device.extract_S11()
    vna.save2s1p(["Hz","S","RI","R 50"], [f,real,imag],"measure"+str(nm))
    
    fig, ax = plot.subplots()  # Create a figure containing a single axes.
    ax.plot(f, real, label = "real")  # Plot some data on the axes.
    ax.plot(f, imag, label = "imaginary")  # Plot some data on the axes.
    
    ax.set_xlabel("Real")  # Add an x-label to the axes.
    ax.set_ylabel("Imaginary")  # Add a y-label to the axes.
    ax.set_title("Teste")  # Add a title to the axes.
    ax.legend()  # Add a legend.
    ax.axis([-1,1,-1,1])
    plot.show()

    pos.small_step_foward()

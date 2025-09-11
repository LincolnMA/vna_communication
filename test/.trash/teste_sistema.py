# vvvvv importing package
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import nanovna as vna
from driver_lib import positioner
import matplotlib.pyplot as plot

import time
'''
roteiro de teste:
1. Conectar do vna ao pc    ok
2. calibrar e salvar a calibração do vna    ok
3. colocar antena no posicionador   ok
4. conectar vna e posicionador  ok
5. carregar calibração ok
6. mover o posicionador
7. fazer medida 
8. mostrar gráfico
9. voltar para a etapa 6
'''
driver = positioner()
driver.connect('/dev/ttyUSB1')
print("connected to driver")
lite = vna.Nvna(baudrate=2e6, port_name='/dev/ttyACM0')
lite.load_calib('./measures/calibration/teste-save-calib.s1p')

#definindo parametros de medicao
fs = 3e9
fe = 6e9
n_points = 250
nmpp = 5

plot.ion()
fig = plot.figure()  # Create a figure containing a single axes.
ax = fig.add_subplot(111)



ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend. 

for i in range(60):
    driver.small_step_foward()
    lite.measure(fs,fe,n_points,nmpp)
    
    lite.calibrate_S11()
    f,r,imag = lite.extract_S11()

    vna.save2s1p(["Hz","S","RI","R 50"],[f,r,imag],f"teste_completo/{i}") 

    f = [freq/10e9 for freq in f]
    ax.clear()
    ax.plot(f,imag,label = "real")

    fig.canvas.draw()
    fig.canvas.flush_events()
    plot.pause(0.05)

driver.disconnect()
lite.close()

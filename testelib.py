import nanovna as vna
import math
import matplotlib.pyplot as plot

a = vna.Nvna(3)#Teste com VNA de verdade

a.calibration(50e3,#Frequência inicial
        6e9, #frequência final
        1000,#Nº de pontos
        5)
print("Insira a antena e pressione enter...")
x = input()
#a.measure(3000000000,11764705,51,5)#gera valores de 3 a 6 GHz com 255 pontos e 1 repetições
a.measure(50e3,#Frequência inicial
        6e9, #frequÊncia final
        1000,#Nº de pontos
        5)   #Nº de medidas por ponto

#S11 e S21 são variáveis complexas
f1,abs_s11_cal = a.extract("S11_CAL")
f2,abs_s11_raw = a.extract("S11_RAW")

f1_GHz = [i/1000000000 for i in f1]
f2_GHz = f1_GHz

fig, ax = plot.subplots()  # Create a figure containing a single axes.
ax.plot(f1_GHz, abs_s11_raw, label = "S11 RAW")  # Plot some data on the axes.
ax.plot(f2_GHz, abs_s11_cal, label = "S11 CAL")
ax.set_xlabel("Frequency in GHz")  # Add an x-label to the axes.
ax.set_ylabel("dB")  # Add a y-label to the axes.
ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend.
plot.show()

a.close()

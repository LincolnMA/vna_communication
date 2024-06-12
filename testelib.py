import nanovna as vna
import math
import matplotlib.pyplot as plot

a = vna.Nvna(3)#Teste com VNA de verdade

#a.measure(3000000000,11764705,51,5)#gera valores de 3 a 6 GHz com 255 pontos e 1 repetições
a.measure(50e3,#Frequência inicial
        6e9, #frequÊncia final
        1000,#Nº de pontos
        5)   #Nº de medidas por ponto

#S11 e S21 são variáveis complexas
f1,s11 = a.extract("S11")
f2,s21 = a.extract("S21")

abs_s11 = [10*math.log10(abs(i)) for i in s11]
abs_s21 = [10*math.log10(abs(i)) for i in s21]
f1_GHz = [i/1000000000 for i in f1]
f2_GHz = f1_GHz

fig, ax = plot.subplots()  # Create a figure containing a single axes.
ax.plot(f1_GHz, abs_s11, label = "S11")  # Plot some data on the axes.
ax.plot(f2_GHz, abs_s21, label = "S21")
ax.set_xlabel("Frequency in GHz")  # Add an x-label to the axes.
ax.set_ylabel("dB")  # Add a y-label to the axes.
ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend.
plot.show()

a.close()

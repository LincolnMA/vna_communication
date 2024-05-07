import nanovna as vna
import math
import matplotlib.pyplot as plot

a = vna.Nvna(3)#Teste com VNA de verdade
#Versão no NanoVNA: V2 vai de 50KHz-3GHz, V3 vai de 1MHz-6GHz
#a = vna.Nvna(3,baudrate=9600)#Teste com Arduino 

a.measure(1000000000,1000000000,2,1)#valores usados no excel, na mesma ordem
a.close()
#S11 e S21 são variáveis complexas
f1,s11 = a.extract("S11")
f2,s21 = a.extract("S21")

abs_s11 = [-10*math.log10(abs(i)) for i in s11]
abs_s21 = [-10*math.log10(abs(i)) for i in s11]
f1_GHz = [i/1000000000 for i in f1]
f2_GHz = f1_GHz

fig, ax = plot.subplots()  # Create a figure containing a single axes.
ax.plot(f1_GHz, abs_s11, label = "S11")  # Plot some data on the axes.
ax.plot(f1_GHz, abs_s21, label = "S21")
ax.set_xlabel("Frequency in GHz")  # Add an x-label to the axes.
ax.set_ylabel("dB")  # Add a y-label to the axes.
ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend.
plot.show()


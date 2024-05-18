import nanovna as vna
import matplotlib.pyplot as plot

a = vna.Nvna(3)#Teste com VNA de verdade
#Versão no NanoVNA: V2 vai de 50KHz-3GHz, V3 vai de 1MHz-6GHz
#a = vna.Nvna(3,baudrate=9600)#Teste com Arduino 

a.measure(3000000000,11764705,255,1)#gera valores de 3 a 6 GHz com 255 pontos
a.close()

abs_s11 = a.get_abs("S11")
abs_s21 = a.get_abs("S21")

f_GHz = a.get_freqs()

fig, ax = plot.subplots()  # Create a figure containing a single axes.
ax.plot(f_GHz, abs_s11, label = "S11")  # Plot some data on the axes.
ax.plot(f_GHz, abs_s21, label = "S21")
ax.set_xlabel("Frequency in GHz")  # Add an x-label to the axes.
ax.set_ylabel("dB")  # Add a y-label to the axes.
ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend.
plot.show()


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
a.calibrate_S11()
freqs,p_real,p_imag = a.extract_SMITH_CAL()
vna.save2s1p(["Hz","S","RI","R 50"],        #Cabeçalhos
         [freqs,p_real,p_imag],         #colunas
         "teste")                       #nome do arquivo

fig, ax = plot.subplots()  # Create a figure containing a single axes.
ax.plot(p_real, p_imag, label = "SMITH")  # Plot some data on the axes.
ax.set_xlabel("Real")  # Add an x-label to the axes.
ax.set_ylabel("Imaginary")  # Add a y-label to the axes.
ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend.
ax.axis([-1,1,-1,1])
plot.show()

a.close()

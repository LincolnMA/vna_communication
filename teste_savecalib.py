import nanovna as vna
import math
import matplotlib.pyplot as plot


freq_init = 3e9
freq_final = 6e9
points_measure = 500
mpp = 5  # measure per points


device = vna.Nvna(3, baudrate=2e6)  # Teste com VNA de verdade


action = input("Save (s) or load (l) ? ")
if action == 's':
    device.calibration(freq_init,  # Frequência inicial
                       freq_final,  # frequência final
                       points_measure,  # Nº de pontos
                       mpp)
    device.save_calib('teste-save-calib')
else:
    device.load_calib('./measures/calibration/teste-save-calib.s1p')
    
input("insira a antena")
device.measure(freq_init, freq_final, points_measure, mpp)
device.calibrate_S11()

f, real, imag =  device.extract_S11()
f = [a/1000000000 for a in f]
print(f)

print(real)
fig, ax = plot.subplots()  # Create a figure containing a single axes.
ax.plot(f, real, label="real")  # Plot some data on the axes.
ax.plot(f, imag, label="imaginary")  # Plot some data on the axes.

ax.set_xlabel("freqs")  # Add an x-label to the axes.
ax.set_ylabel("value")  # Add a y-label to the axes.
ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend.
plot.show()

device.close()

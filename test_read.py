import nanovna
import matplotlib.pyplot as plot




_freqs = [1,2000000000000000,3]
_e00 = [complex(1,2),complex(1,2),complex(1,2)]
_e01 = [complex(1,2),complex(1,2),complex(1,2)]
_e11 = [complex(1,2),complex(1,2),complex(1,2)]
e00_real = [c.real for c in _e00]
e00_imag = [c.imag for c in _e00]
e01_real = [c.real for c in _e01]
e01_imag = [c.imag for c in _e01]
e11_real = [c.real for c in _e11]
e11_imag = [c.imag for c in _e11]

nanovna.save2s1p(
            ['Hz','S','RI','e00','e01','e11'],
            [_freqs,
             e00_real,e00_imag,
             e01_real,e01_imag,
             e11_real,e11_imag
             ],
            'teste1-savecalib'
        )



header, data = nanovna.read_s1p('./measures/erik1.s1p')

f = data[0]
r = data[1]
i = data[2]

fig, ax = plot.subplots()  # Create a figure containing a single axes.
ax.plot(f, r, label = "S11 CAL real")  # Plot some data on the axes.
ax.plot(f, i, label = "S11 CAL imag")  # Plot some data on the axes.
    
ax.set_xlabel("Frequency in GHz")  # Add an x-label to the axes.
ax.set_ylabel("dB")  # Add a y-label to the axes.
ax.set_title("Teste")  # Add a title to the axes.
ax.legend()  # Add a legend.
plot.show()
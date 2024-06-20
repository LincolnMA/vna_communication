import nanovna




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



header, data = nanovna.read_s1p('./measures/teste1-savecalib.s1p')
print([d[0] for d in data])

print(header)
for d in data:
    print(d)
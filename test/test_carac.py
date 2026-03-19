from vna_driver import vna_driver, read_s1p
from pathlib import Path


lite = vna_driver()


lite.connect(port_name = "/dev/ttyACM0")
lite.cfg_sweep(start = 1e9, stop = 6e9, points = 401, n_mean = 2)

lite.measure()
print(lite._S11_RAW)
print(lite._freqs)

a = open('tampapreta_litevna.s1p','w')

for i in range(len(lite._freqs)):
    a.write(f'{lite._freqs[i]}\t{lite._S11_RAW[i].real}\t{lite._S11_RAW[i].imag}\n')

lite.close()

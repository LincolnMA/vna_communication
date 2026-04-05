from vna_driver import vna_driver
import matplotlib.pyplot as plt

def test_varredura1():
    vna = vna_driver()
    
    vna.connect('dadaw')
    vna.cfg_sweep(start = 3e9, stop = 6e9, points = 201, n_mean = 5)

    vna.measure()

    freq, r, i = vna.extract_s11_raw()


    fig,ax = plt.subplots()

    ax.plot(freq, r)
    ax.plot(freq, i)

    plt.show()


    
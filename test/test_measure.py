import pytest
from vna_driver import vna_driver
import matplotlib.pyplot as plt

lite = vna_driver()


# fixture para desconectar automaticamente
@pytest.fixture(autouse=True)
def close_connection():
    yield
    lite.close()

def test_connect():
    
    result = lite.connect(port_name = "COM8")
    assert result == True



def test_measure_raw():
    lite.connect(port_name = "COM8")
    lite.cfg_sweep(start = 200e6, stop = 3e9, points = 201, n_mean = 5)

    lite.measure()

    freq, s11_r_raw, s11_i_raw = lite.extract_s11_raw()
  
    fig, ax_raw = plt.subplots(1)

    ax_raw.plot(freq, s11_r_raw, label = "real")
    ax_raw.plot(freq, s11_i_raw, label = "imag")
    
    plt.legend()
    plt.show()

def test_measure_calib():
    lite.connect(port_name = "COM8")
    lite.cfg_sweep(start = 200e6, stop = 3e9, points = 201, n_mean = 5)

    lite.calibrate_cli()


    lite.measure()

    freq, s11_r_raw, s11_i_raw = lite.extract_s11_raw()
    freq, s11_r, s11_i = lite.extract_s11()
    
    fig, [ax_raw, ax_calib] = plt.subplots(2)

    ax_raw.plot(freq, s11_r_raw, label = "real")
    ax_raw.plot(freq, s11_i_raw, label = "imag")
    

    ax_calib.plot(freq, s11_r, label = "real")
    ax_calib.plot(freq, s11_i, label = "imag")

    plt.legend()
    plt.show()



    
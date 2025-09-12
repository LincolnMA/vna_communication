import pytest
from vna_driver import vna_driver, read_s1p
import matplotlib.pyplot as plt
from pathlib import Path

lite = vna_driver()
cwd = Path.cwd()/'test'

# fixture para desconectar automaticamente
@pytest.fixture(autouse=True)
def close_connection():
    yield
    lite.close()


@pytest.fixture(autouse=True)
def setup(request):

    if 'nosetup' in request.keywords: return 

    lite.connect(port_name = "COM8")
    lite.cfg_sweep(start = 300e6, stop = 5e9, points = 201, n_mean = 2)
    yield
    lite.close()

@pytest.mark.nosetup
def test_connect():
    
    result = lite.connect(port_name = "COM8")
    assert result == True



def test_measure_raw_s11():

    lite.measure()

    freq, s11_r_raw, s11_i_raw = lite.extract_s11_raw()
  
    fig, ax_raw = plt.subplots(1)

    ax_raw.plot(freq, s11_r_raw, label = "real")
    ax_raw.plot(freq, s11_i_raw, label = "imag")

    plt.title("raw s11")
    plt.legend()
    plt.show()

def test_measure_raw_s11_logmag():
    
    lite.measure()
    freq, s11_logmag_raw = lite.extract_s11_raw_logmag()

    fig, ax = plt.subplots(1)

    ax.plot(freq,s11_logmag_raw)

    plt.title("S11 log mag")
    plt.show()



def test_measure_calib():

    lite.calibrate_cli()

    input("Put the mut")

    lite.measure()

    freq, s11_r_raw, s11_i_raw = lite.extract_s11_raw()
    freq, s11_r, s11_i = lite.extract_s11()
    
    freq1, s11_logmag = lite.extract_s11_logmag()

    fig, [ax_raw, ax_calib] = plt.subplots(2)
    fig2, ax_logmag = plt.subplots(1)

    ax_raw.plot(freq, s11_r_raw, label = "real")
    ax_raw.plot(freq, s11_i_raw, label = "imag")
    

    ax_calib.plot(freq, s11_r, label = "real")
    ax_calib.plot(freq, s11_i, label = "imag")

    ax_logmag.plot(freq1, s11_logmag, label = "logmag")

    plt.legend()
    plt.show()


def test_save_calib():

    lite.calibrate_cli()
    lite.save_calib(cwd/"calib_test.s1p")
    

def test_measure_load_calib():
    lite.load_calib(cwd/'calib_test.s1p')
    lite.measure()

    freq, s11_raw_logmag = lite.extract_s11_raw_logmag()
    freq, s11_logmag = lite.extract_s11_logmag()

    fig, [axraw, axcalib] = plt.subplots(2)

    axraw.plot(freq, s11_raw_logmag, label = "raw")
    axcalib.plot(freq, s11_logmag, label = "calib")


    fig.tight_layout()

    plt.title("Load calib")
    plt.legend()
    plt.show()



def test_save_s11():
    lite.load_calib(cwd/'calib_test.s1p')
    lite.measure()

    lite.save_s11(cwd/'teste.s1p')

    _, data = read_s1p(cwd/'teste.s1p')

    freqs = data[0]
    r = data[1]
    i = data[2]
    
    fig, ax = plt.subplots(1)

    ax.plot(freqs, r)
    ax.plot(freqs, i)

    plt.title("save s11")
    plt.show()

def test_save_logmag_s11():
    lite.load_calib(cwd/'calib_test.s1p')
    lite.measure()

    f = cwd/'test_logmag.s1p'
    lite.save_s11_logmag(f)

    _, data = read_s1p(f)

    freqs = data[0]
    logmag = data[1]
    
    fig, ax = plt.subplots(1)

    ax.plot(freqs, logmag)


    plt.title("save logmag")
    plt.show()



 

    
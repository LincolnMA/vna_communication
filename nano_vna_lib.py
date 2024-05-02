import serial
import serial.tools.list_ports

class NanoVNA:

    def __init__(self,
                 version = 3,
                 port_name = None,
                 baudrate = 115200,
                 start_freq = 0,
                 sweepStartHz = None,
                 sweepStepHz = None,
                 valuesPerFrequency = 1):
        

    _freqs = []
    _S11 = []
    _S21 = []
    
    _fwd0Re = []
    _fwd0Im = []
    
    _rev0Re = []
    _rev0Im = []
    
    _rev1Re = []
    _rev1Im = []
    
    _freqIndex = []
    
    port = None
    baudrate = None
    connection = serial.Serial()

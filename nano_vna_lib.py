import serial
import serial.tools.list_ports

class NanoVNA:
    
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
    
    connection = serial.Serial()

    def __init__(self,
                 version = 3,
                 port_name = None,
                 baudrate = 115200):
        
        print("conectando...")
        if not self.connection.is_open:
            if port_name == None:
                ports_name = find_port_name(self)##Falta
            self.connection.port = port_name
            self.connection.baudrate = baudrate
            self.connection.parity = serial.PARITY_NONE
            self.connection.stopbits = serial.STOPBITS_ONE
            self.connection.timeout = 1
            self.connection.open()
    def __str__(self):
        return f"Em construção"

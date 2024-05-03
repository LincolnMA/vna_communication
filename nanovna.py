import serial
import serial.tools.list_ports

class Nvna:
    #Variáveis privadas
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
    
    _connection = serial.Serial()
    #Métodos
       
    def __init__(self,
                 version = 3,#V2 vai de 50KHz-3GHz, V3 vai de 1MHz-6GHz 
                 port_name = None,
                 baudrate = 115200):
        
        print("conectando...")
        if not self._connection.is_open:
            if port_name == None:
                port_name = find_port()
            self._connection.port = port_name
            self._connection.baudrate = baudrate
            self._connection.parity = serial.PARITY_NONE
            self._connection.stopbits = serial.STOPBITS_ONE
            self._connection.timeout = 1
            self._connection.open()
    def __str__(self):
        return f"Em construção"
    def measure(self,
                sweepStartHz,           #Sets the sweep start frequency in Hz. uint64. 
                sweepStepHz,            #Sets the sweep step frequency in Hz. uint64.
                sweepPoints,            #Sets the number of sweep frequency points. uint16.
                valuesPerFrequency):    #Sets the number of data points for each frequency. uint16.
        command = bytearray([int(0x23)])#comando
        command += bytearray([int(0x00)])#endereço
        command += sweepStartHz.to_bytes(length=8, byteorder='little', signed=False)
        command += bytearray([int(0x23)])#comando
        command += bytearray([int(0x10)])#endereço
        command += sweepStepHz.to_bytes(length=8, byteorder='little', signed=False)
        command += bytearray([int(0x21)])#comando
        command += bytearray([int(0x20)])#endereço
        command += sweepPoints.to_bytes(length=2, byteorder='little', signed=False)
        command += bytearray([int(0x21)])#comando
        command += bytearray([int(0x22)])#endereço
        command += valuesPerFrequency.to_bytes(length=2, byteorder='little', signed=False)
        command += bytearray([int(0x18)])#comando
        command += bytearray([int(0x30)])#endereço
        command += sweepPoints.to_bytes(length=1, byteorder='little', signed=False)
        self._connection.write(command)
        #Substituir por uma função f(comando,endereço,length,valor)
        #colocar command como propriedade do objeto




def find_port():
    ports = serial.tools.list_ports.comports()
    n_ports = len(ports)
    if n_ports == 0: print("Não há portas conectadas!")
    if n_ports == 1: print("VNA em " + ports[0].device)
    if n_ports > 1: pass #Ainda não implementado
    return ports[0].device

import serial
import serial.tools.list_ports
import time

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

    _raw = []
    
    _connection = serial.Serial()
    _version = None
    #Métodos
       
    def __init__(self,
                 version = 3,#V2 vai de 50KHz-3GHz, V3 vai de 1MHz-6GHz 
                 port_name = None,
                 baudrate = 115200):
        
        print("conectando...")
        self._version = version
        if self._connection.is_open:
            self._connection.close()
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
        
        print("Configurando Sweep...")
        self.send(0x23,0x0,8,sweepStartHz)
        self.send(0x23,0x10,8,sweepStepHz)
        self.send(0x21,0x20,2,sweepPoints)
        self.send(0x21,0x22,2,valuesPerFrequency)
        self.send(0x18,0x30,1,sweepPoints)#Comando de leitura da fila
        
        waiting_points = sweepPoints*32.0
        delay = waiting_points*8.0/self._connection.baudrate
        print("Aguardando ",2*delay," segundos...")
        time.sleep(2*delay)
        
        if self._connection.in_waiting != sweepPoints*32:
            print("Erro de conexão!")
            print("Esperado ",waiting_points,"bytes, tendo chegado ",self._connection.in_waiting)
            return
        for i in range(0,sweepPoints):
            self._raw.append(self._connection.read(32))
        print(self._raw)
        
    def send(self,
             command,#Comando a ser usado
             address,#Endereço do resgistrador
             length, #Número de bytes a serem enviados
             value): #valor a ser transmitido para o registrador
        
        payload = bytearray([int(command)])#comando
        payload += bytearray([int(address)])#endereço
        payload += value.to_bytes(length=length, byteorder='little', signed=False)
        print(payload)
        if self._connection.is_open:
            self._connection.write(payload)
        else:
            print("Conection Lost!")
    
    def close(self):
        self._connection.close()

def find_port():
    ports = serial.tools.list_ports.comports()
    n_ports = len(ports)
    if n_ports == 0: print("Não há portas conectadas!")
    if n_ports == 1: print("VNA em " + ports[0].device)
    if n_ports > 1: pass #Ainda não implementado
    return ports[0].device
import serial
import serial.tools.list_ports
import time
#falta adicionar toda a parte de calibração
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

    _payload = []
    
    _connection = serial.Serial()
    
    _version = None

    _default_baudrate = 115200
    _default_point_size = 32
    #Métodos
       
    def __init__(self,
                 version = 3,#V2 vai de 50KHz-3GHz, V3 vai de 1MHz-6GHz 
                 baudrate = _default_baudrate,
                 port_name = None):
        
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
        time.sleep(2)#Tempo para estabelecimento de uma conexão serial nova
        
    def __str__(self):
        return f"Em construção"
    def measure(self,
                sweepStartHz,           #Sets the sweep start frequency in Hz. uint64. 
                sweepStepHz,            #Sets the sweep step frequency in Hz. uint64.
                sweepPoints,            #Sets the number of sweep frequency points. uint16.
                valuesPerFrequency):    #Sets the number of data points for each frequency. uint16.
        #Falta checar a versão com as frequências inseridas
        print("Configurando Sweep...")
        self._payload = bytearray()
        self.config_payload(0x23,0x0,8,sweepStartHz)
        self.config_payload(0x23,0x10,8,sweepStepHz)
        self.config_payload(0x21,0x20,2,sweepPoints)
        self.config_payload(0x21,0x22,2,valuesPerFrequency)
        self.config_payload(0x18,0x30,1,sweepPoints)#Comando de leitura da fila
        print(self._payload)
        if self._connection.is_open:
            self._connection.write(self._payload)
            self._connection.flush()
        else:
            print("Conection Lost!")
        
        f = list(range(0,sweepPoints))
        self._freqs = [(i*sweepStepHz)+sweepStartHz for i in f]

        waiting_bytes = sweepPoints*valuesPerFrequency*float(self._default_point_size)
        delay = waiting_bytes*8.0/self._connection.baudrate
        #Falta usar o delay para alterar o timeout da serial, o padrão ainda é 1s
        print("Aguardando ",2*delay," segundos...")
        
        for i in range(0,sweepPoints*valuesPerFrequency):
            self._raw.append(self._connection.read(self._default_point_size))
        print("dados brutos:")
        print(self._raw)

        for i in self._raw:
            self._fwd0Re.append(int.from_bytes(i[0:4],byteorder="little",signed = False))
            self._fwd0Im.append(int.from_bytes(i[4:8],byteorder="little",signed = False))
            self._rev0Re.append(int.from_bytes(i[8:12],byteorder="little",signed = False))
            self._rev0Im.append(int.from_bytes(i[12:16],byteorder="little",signed = False))
            self._rev1Re.append(int.from_bytes(i[16:20],byteorder="little",signed = False))
            self._rev1Im.append(int.from_bytes(i[20:24],byteorder="little",signed = False))
            self._freqIndex.append(int.from_bytes(i[24:26],byteorder="little",signed = False))
        #falta processar uma possível média dos valores quando valuesperfreq for maior que 1
        self._S11 = [complex(self._rev0Re[i],self._rev0Im[i])/
                     complex(self._fwd0Re[i],self._fwd0Re[i]) for i in range(0,sweepPoints)]
        self._S21 = [complex(self._rev1Re[i],self._rev1Im[i])/
                     complex(self._fwd0Re[i],self._fwd0Re[i]) for i in range(0,sweepPoints)]
    def extract(self,par):
        if par == "S11": return [self._freqs,self._S11]
        if par == "S21": return [self._freqs,self._S21]
        
    def config_payload(self,
             command,#Comando a ser usado
             address,#Endereço do resgistrador
             length, #Número de bytes a serem enviados
             value): #valor a ser transmitido para o registrador
        
        self._payload += bytearray([int(command)])#comando
        self._payload += bytearray([int(address)])#endereço
        self._payload += value.to_bytes(length=length, byteorder='little', signed=False)
    
    def close(self):
        self._connection.close()
        

def find_port():
    ports = serial.tools.list_ports.comports()
    n_ports = len(ports)
    if n_ports == 0: print("Não há portas conectadas!")
    if n_ports == 1: print("VNA em " + ports[0].device)
    if n_ports > 1: pass #Ainda não implementado
    return ports[0].device

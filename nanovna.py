import serial
import serial.tools.list_ports
import time
import struct
#falta adicionar toda a parte de calibração
class Nvna:

    #Código de Operação dos comandos
    
    NOP = 0X00 #No operation
    INDICATE = 0X0d #Device always replies with ascii '2'(0x32)
    
    READ = 0X10 #Read a 1-byte register at address AA.Reply is one byte, the read value.
    READ2 = 0X11 #Read a 2-byte register at address AA.Reply is 2 bytes, the read value.
    READ4 = 0X12 #Read a 4-byte register at address AA.Reply is 4 bytes, the read value.
    READFIFO = 0X18 #Read NN values from a FIFO at address AA.Reply is the read values in order.Each value can be more than one byte and is determined by the FIFO being read.
    
    WRITE = 0X20 #Write XX to a 1-byte register at address AA.There is no reply.
    WRITE2 = 0X21 #Write X0 to AA, then X1 to AA+1.There is no reply.
    WRITE4 = 0X22 #Write X0..X3 to registers starting at AA. There is no reply.
    WRITE8 = 0X23 #This command is 10 bytes in total.Bytes 2..9 correspond to X0..X7.Write X0..X7 to registers starting at AA.There is no reply.
    WRITEFIFO = 0X28 #Write NN bytes into a FIFO at address AA.NN bytes of data to be written into the FIFO should follow “NN".There is no reply.

    #Registradores
    REGsweepStartHz = 0X00 #Sets the sweep start frequency in Hz. uint64
    REGsweepStepHz = 0X10 #Sets the sweep step frequency in Hz. uint64
    REGsweepPoints = 0X20 #Sets the number of sweep frequency points. uint16
    REGvaluesPerFrequency = 0X22 #Sets the number of data points to output for each frequency.uint16.
    REGrawSamplesMode = 0x26 #Writing 1 switches USB data format to raw samples mode and leaves this protocol.
    REGvaluesFIFO = 0x30 #Returns VNA sweep data points. Each value is 32 bytes.Writing any value (using WRITE command) clears the FIFO.
    REGdeviceVariant = 0xf0 #The type of device this is. Always 0x02 for S-A-A-2.
    REGprotocolVersion = 0xf1 #Version of this wire protocol. Always 0x01.
    REGhardwareRevision = 0xf2 #Hardware revision.
    REGfirmwareMajor = 0xf3 #Firmware major version.
    REGfirmwareM = 0xf4 #Firmware minor version.

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
                     #Talvez não precise com o equipamento real
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
        self.config_payload(self.WRITE,self.REGvaluesFIFO,1,0)
        self.config_payload(self.WRITE8,self.REGsweepStartHz,8,sweepStartHz)
        self.config_payload(self.WRITE8,self.REGsweepStepHz,8,sweepStepHz)
        self.config_payload(self.WRITE2,self.REGsweepPoints,2,sweepPoints)
        self.config_payload(self.WRITE2,self.REGvaluesPerFrequency,2,valuesPerFrequency)
        self.config_payload(self.READFIFO,self.REGvaluesFIFO,1,sweepPoints*valuesPerFrequency)#Comando de leitura da fila
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
        self._connection.timeout = 2*delay
        print("Aguardando um máximo de ",2*delay," segundos...")
        
        for i in range(0,sweepPoints*valuesPerFrequency):
            self._raw.append(self._connection.read(self._default_point_size))
        print("dados brutos:")
        print(self._raw)
        print("faltam ",self._connection.in_waiting, " bytes na fila")

        self._fwd0Re = [0]*sweepPoints
        self._fwd0Im = [0]*sweepPoints
        self._rev0Re = [0]*sweepPoints
        self._rev0Im = [0]*sweepPoints
        self._rev1Re = [0]*sweepPoints
        self._rev1Im = [0]*sweepPoints
        for i in self._raw:
            
            unpacked_data = struct.unpack("<6lH6s",i)
            """
                Estrutura do dados (32bytes little endian): 
                    fwd0Re int32
                    fwd0Im int32
                    rev0Re int32
                    rev0Im int32
                    rev1Re int32
                    rev1Im int32
                    freqIndex uint16
                    reserved (falta descobrir oque é) 6bytes 
            """
            self._freqIndex = unpacked_data[6]
            print("index = ",self._freqIndex)
            self._fwd0Re[self._freqIndex] += unpacked_data[0]
            self._fwd0Im[self._freqIndex] += unpacked_data[1]
            self._rev0Re[self._freqIndex] += unpacked_data[2]
            self._rev0Im[self._freqIndex] += unpacked_data[3]
            self._rev1Re[self._freqIndex] += unpacked_data[4]
            self._rev1Im[self._freqIndex] += unpacked_data[5]
        
        self._fwd0Re = [i/valuesPerFrequency for i in self._fwd0Re]
        self._fwd0Im = [i/valuesPerFrequency for i in self._fwd0Im]
        self._rev0Re = [i/valuesPerFrequency for i in self._rev0Re]
        self._rev0Im = [i/valuesPerFrequency for i in self._rev0Im]
        self._rev1Re = [i/valuesPerFrequency for i in self._rev1Re]
        self._rev1Im = [i/valuesPerFrequency for i in self._rev1Im]
        
        self._S11 = [complex(0,0)]*sweepPoints
        self._S21 = [complex(0,0)]*sweepPoints
        for i in range(0,sweepPoints):
            try:
                self._S11[i] = complex(self._rev0Re[i],self._rev0Im[i]) /\
                               complex(self._fwd0Re[i],self._fwd0Im[i])
            except ZeroDivisionError:
                self._S11[i] = complex(1,0)
        
            try:
                self._S21[i] = complex(self._rev1Re[i],self._rev1Im[i]) /\
                               complex(self._fwd0Re[i],self._fwd0Im[i])
            except ZeroDivisionError:
                self._S21[i] = complex(1,0)

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

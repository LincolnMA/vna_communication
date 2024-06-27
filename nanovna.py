import serial
import serial.tools.list_ports
import time
import struct
import math

class Nvna:

    #Operation codes
    
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

    #Registers
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

    _freqs = []     #Frequency vector, in Hz
    _S11_RAW = []   #S11 uncalibrated
    _S21_RAW = []   #S22 uncalibrated

    _S11_CAL = []   #s11 calibrated
    
    _fwd0Re = []    #real part of foward wave from port 1
    _fwd0Im = []    #imaginary part of foward wave from port 1
    
    _rev0Re = []    #real part of reflected wave
    _rev0Im = []    #imaginary part of reflected wave
    
    _rev1Re = []    #real part of S21
    _rev1Im = []    #imaginary part of S21
    
    _freqIndex = [] #index of measures comming from each sweep

    _raw = []       #raw data from each sweep

    _payload = []   #packet of data contain all commands to start a sweep 
    
    _connection = serial.Serial()
    
    _version = None

    _default_baudrate = 115200
    _default_point_size = 32
    #Variáveis de calibração
    _e00 = None
    _e01 = None
    _e10 = None
    _e11 = None
    _cal = False    #flag que indica se foi calibrado
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
        #time.sleep(2)#Tempo para estabelecimento de uma conexão serial nova
                     #Talvez não precise com o equipamento real


    def __str__(self):
        return f"Em construção"
    

    def measure(self,start_f,end_f,n_points,nmpp):

        self._S11_RAW = []
        self._S21_RAW = []
        self._freqs = []

        total_points = int( n_points*nmpp )
        step = int( (end_f - start_f)/n_points)
        if total_points <= 255:#max value to one fifo read
            self.sweep(start_f,step,n_points,nmpp)
            return
        #Determina o número de frequênicas diferentes que cabem em um sweep, menos o último 
        n_freqs_per_measure = math.floor(255/nmpp)
        #determina o número de frequêncas na última medida
        n_freqs_last_measure = n_points%n_freqs_per_measure 
        #determina o número de sweeps, menos o último
        n_measures = math.floor(n_points/n_freqs_per_measure)
        #realização das medidas de maneira consecutiva
        for i in range(0,n_measures):
            print("medição ",i)
            self.sweep(int( start_f + (i*step*n_freqs_per_measure) ),
                         int( step ),
                         int( n_freqs_per_measure ),
                         int( nmpp ))
            #a = input()
        #Última medição
        self.sweep(int( start_f + n_measures*step*n_freqs_per_measure ),
                     int( step ),
                     int( n_freqs_last_measure ),
                     int( nmpp ))
        

    def sweep(self,
                sweepStartHz,           #Sets the sweep start frequency in Hz. uint64. 
                sweepStepHz,            #Sets the sweep step frequency in Hz. uint64.
                sweepPoints,            #Sets the number of sweep frequency points. uint16.
                valuesPerFrequency):    #Sets the number of data points for each frequency. uint16.
        #Falta checar a versão com as frequências inseridas
        print("Configurando Sweep...")
        print("( ",
              sweepStartHz,           #Sets the sweep start frequency in Hz. uint64. 
              sweepStepHz,            #Sets the sweep step frequency in Hz. uint64.
              sweepPoints,            #Sets the number of sweep frequency points. uint16.
              valuesPerFrequency," )")
        self._payload = bytearray()
        self.config_payload(self.WRITE,self.REGvaluesFIFO,1,0)
        self.config_payload(self.WRITE8,self.REGsweepStartHz,8,sweepStartHz)
        self.config_payload(self.WRITE8,self.REGsweepStepHz,8,sweepStepHz)
        self.config_payload(self.WRITE2,self.REGsweepPoints,2,sweepPoints)
        self.config_payload(self.WRITE2,self.REGvaluesPerFrequency,2,valuesPerFrequency)
        self.config_payload(self.READFIFO,self.REGvaluesFIFO,1,sweepPoints*valuesPerFrequency)#Comando de leitura da fila
        #print(self._payload)
        if self._connection.is_open:
            self._connection.write(self._payload)
            self._connection.flush()
        else:
            print("Conection Lost!")
        
        f = list(range(0,sweepPoints))
        freqs = [(i*sweepStepHz)+sweepStartHz for i in f]

        waiting_bytes = sweepPoints*valuesPerFrequency*float(self._default_point_size)
        delay = waiting_bytes*8.0/self._connection.baudrate
        self._connection.timeout = 2*delay
        print("Aguardando um máximo de ",2*delay," segundos...")
        
        self._raw = []
        for i in range(0,sweepPoints*valuesPerFrequency):
            self._raw.append(self._connection.read(self._default_point_size))
        #print("dados brutos:")
        #print(self._raw)
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
            #print("index = ",self._freqIndex)
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
        
        S11 = [complex(0,0)]*sweepPoints
        S21 = [complex(0,0)]*sweepPoints
        for i in range(0,sweepPoints):
            try:
                S11[i] = complex(self._rev0Re[i],self._rev0Im[i]) /\
                               complex(self._fwd0Re[i],self._fwd0Im[i])
            except ZeroDivisionError:
                S11[i] = complex(1,0)
        
            try:
                S21[i] = complex(self._rev1Re[i],self._rev1Im[i]) /\
                               complex(self._fwd0Re[i],self._fwd0Im[i])
            except ZeroDivisionError:
                S21[i] = complex(1,0)
        self._S11_RAW.extend(S11)
        self._S21_RAW.extend(S21)
        self._freqs.extend(freqs)

    def extract_S11_RAW(self):
        return [self._freqs,to_db(self._S11_RAW)]

    def extract_S21_RAW(self):
        return [self._freqs,to_db(self._S21_RAW)]

    def extract_S11_CAL(self):
        return [self._freqs,to_db(self._S11_CAL)]
    
    def extract_SMITH_RAW(self):
        R = [i.real for i in self._S11_RAW]
        I = [i.imag for i in self._S11_RAW]
        return [self._freqs,R,I]
    
    def extract_SMITH_CAL(self):
        module = [abs(i) for i in self._S11_CAL]
        max_module = max(module)
        R = [i.real/max_module for i in self._S11_CAL]
        I = [i.imag/max_module for i in self._S11_CAL]
        return [self._freqs,R,I]

    #Não implementado ainda vvvvvvvvvvvvvvvvvvv
    """
    #essa daqui precisa medir o throught,
    def extract_S21CAL(self):
        pass
    
    def extract_phase(self):
        pass
    """

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

    #calbration methods vvvvvv

    def calibration(self,start_f,end_f,n_points,nmpp):
        
        print("Insert short and press enter...")
        a = input()
        self.measure(start_f,end_f,n_points,nmpp)
        s11_short = self._S11_RAW
        s21_short = self._S21_RAW

        print("Insert open and press enter...")
        a = input()
        self.measure(start_f,end_f,n_points,nmpp)
        s11_open = self._S11_RAW
        s21_open = self._S21_RAW

        print("Insert load and press enter...")
        a = input()
        self.measure(start_f,end_f,n_points,nmpp)
        s11_load = self._S11_RAW
        s21_load = self._S21_RAW
        """
        print("Insert throw and press enter...")
        a = input()
        self.measure(start_f,end_f,n_points,nmpp)
        s11_throw = self.extract("S11_RAW")
        s21_throw = self.extract("S21_RAW")
        """

        self._e00 = s11_load
        self._e11 = [complex(0,0)]*len(self._e00)
        self._e01 = [complex(0,0)]*len(self._e00)
        for i in range(len(self._e00)):
            self._e11[i] = (s11_open[i] + s11_short[i] - 2*s11_load[i])/(s11_open[i] - s11_short[i])
            self._e01[i] = (1-self._e11[i]**2)*(s11_open[i] - s11_short[i])/2

        print("Calibrated!")
        self._cal = True


    def calibrate_S11(self):
        if not self._cal:
            print("Sem Calibração!")
            self._S11_CAL =  [0 for i in self._S11_RAW]
        self._S11_CAL = [complex(0,0)]*len(self._e00) 
        for i in range(len(self._e00)):
            temp = self._S11_RAW[i] - self._e00[i]
            self._S11_CAL[i] = (temp)/(self._e01[i] + self._e11[i]*temp)
        return [self._freqs,to_db(self._S11_CAL)]
    def save_calib(self,filename):
        if self._cal == False: 
            raise Exception("You haven't calibrated yet! Please calibrate or load calibration data")
        
        e00_real = [c.real for c in self._e00]
        e00_imag = [c.imag for c in self._e00]
        e01_real = [c.real for c in self._e01]
        e01_imag = [c.imag for c in self._e01]
        e11_real = [c.real for c in self._e11]
        e11_imag = [c.imag for c in self._e11]


        save2s1p(
            ['Hz','S','RI','e00','e01','e11'],
            [self._freqs,
             e00_real,e00_imag,
             e01_real,e01_imag,
             e11_real,e11_imag
             ],
            '/calibration/'+filename
        )
    def load_calib(self,path):
        header, data = read_s1p(path)
        self._freqs = data[0]
        e00_real = data[1]
        e00_imag = data[2]
        e01_real = data[3]
        e01_imag = data[4]
        e11_real = data[5]
        e11_imag = data[6]

        e00 = []
        e01 = []
        e11 = []

        for i in range(len(e00)):
            e00.append(complex(e00_real[i], e00_imag[i]))
            e01.append(complex(e01_real[i],e01_imag[i]))
            e11.append(complex(e11_real[i],e11_imag[i]))

        self._e00 = e00
        self._e01 = e01
        self._e11 = e11

        self._cal = True

def find_port():
    ports = serial.tools.list_ports.comports()
    n_ports = len(ports)
    if n_ports == 0: print("Não há portas conectadas!")
    if n_ports == 1: print("VNA em " + ports[0].device)
    if n_ports > 1: pass #Ainda não implementado
    return ports[0].device

def to_db(val):
    return [20*math.log10(abs(i)) for i in val]

def save2s1p(headers,values,filename):
    f = open("measures/" + filename + ".s1p", "w")
    f.write("! Saved from nanovna library\n")
    
    f.write("#")
    for i in headers: f.write(" " + i)
    f.write("\n")

    for i in range( len(values[0]) ):
        for j in range( len(values) ):
            if j == 0:
                f.write( f'{values[j][i]:10}\t' )
            else:
                f.write( f'{values[j][i]:.11f}\t' )
        f.write("\n")
    
    f.close()

def read_s1p(path):
    file = open(path,'r')
    content = file.read()
    file.close()

    content = content.split('\n') #separar por linhas
    header_line = 0
    for line in content:

        if '#' in line:
            break
        header_line += 1
    
    header = content[header_line]
    header = header.split(' ')
    header.pop(0) #remove '#'

    raw = content[header_line+1:]
    raw = [line.split('\t') for line in raw]

    data = []
    
    for line in raw:
        d = []
        for item in line:
            if item != '': d.append(float(item))
        if d != []: data.append(d)

    data_transposed = [] # transpondo a matriz, os dados vem em colunas, então teremos uma coluna para cada parametro, ao invés de uma linha para cada 

    for i in range(len(data)):
        data_transposed.append([d[i] for d in data])

    return header, data_transposed
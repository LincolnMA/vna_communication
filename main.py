import serial
import serial.tools.list_ports
import tkinter as tk
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#funções
def connect():
    print("conectando...")
    global connection
    if connection.is_open: return
    
    selected = selected_port.get().split(":")
    port_name = selected[0]
    connection.port = port_name
    if platform.system() == "Linux": 
        connection.port = "/dev/" + connection.port
    
    connection.baudrate = int(ent1.get())
    
    selected = selected_parity.get().split(":")
    if selected == "N": 
        connection.parity = serial.PARITY_NONE
    elif selected == "E":
        connection.parity = serial.PARITY_EVEN
    else:
        connection.parity = serial.PARITY_ODD

    selected = selected_stopbits.get()
    if selected == "1":
        connection.stopbits = serial.STOPBITS_ONE
    else:
        connection.stopbits = serial.STOPBITS_TWO

    connection.timeout = float(ent2.get())
    connection.open()
def desconnect():
    print("Desconectando...")
    global connection
    if not connection.is_open: return
    connection.close()
def send():
    print("Enviando...")
    global connection
    if not connection.is_open: return
    commands = hex_in.get().split("-")
    byte_array = bytes([int(x,16) for x in commands])
    connection.write(byte_array)
def rec():
    print("Recebendo...")
    global connection
    if not connection.is_open: return
    byte_array = connection.read(connection.in_waiting)
    hex_out.delete(0,tk.END)
    hex_out.insert(0,byte_array.hex())
def plotar():
    print("plotar")

#variáveis
root = tk.Tk()

connection = serial.Serial()

port_options = []
ports = serial.tools.list_ports.comports()
if len(ports) > 0:
    port_options = [i.name + ": " + i.manufacturer for i in ports]
else:
    port_options.append("Sem portas")
selected_port = tk.StringVar()
selected_port.set(port_options[0])

parity_options = ["N: None","E: Even","O: Odd"]
selected_parity = tk.StringVar()
selected_parity.set(parity_options[0])

stopbits_options = ["1","2"]
selected_stopbits = tk.StringVar()
selected_stopbits.set(stopbits_options[0])

fig, ax = plt.subplots()

#interface

fr = tk.Frame(root)
fr.grid(row = 0,column = 0)

fr1 = tk.LabelFrame(fr,text = "Configuração")
fr1.grid(row = 0,column = 0)

fr2 = tk.LabelFrame(fr,text = "Transmissão Manual")
fr2.grid(row = 1,column = 0)

fr3 = tk.LabelFrame(fr,text = "Transmissão Automática")
fr3.grid(row = 2,column = 0)

tx1 = tk.Label(fr1,text = "Porta")
tx1.grid(row = 0,column = 0)
menu_ports = tk.OptionMenu(fr1, selected_port,*port_options)
menu_ports.grid(row = 0,column = 1)

tx2 = tk.Label(fr1,text = "Baudrate (bits por segundo)")
tx2.grid(row = 1,column = 0)
ent1 = tk.Entry(fr1)
ent1.insert(0,"9600")
ent1.grid(row = 1,column = 1)

tx5 = tk.Label(fr1, text = "Paridade")
tx5.grid(row = 2,column = 0)
menu_parity = tk.OptionMenu(fr1,selected_parity,*parity_options)
menu_parity.grid(row = 2,column = 1)

tx3 = tk.Label(fr1,text = "Stop Bits")
tx3.grid(row = 3,column = 0)
menu_stopbits = tk.OptionMenu(fr1,selected_stopbits,*stopbits_options)
menu_stopbits.grid(row = 3,column = 1)

tx4 = tk.Label(fr1,text = "Timeout (segundos)")
tx4.grid(row = 4,column = 0)
ent2 = tk.Entry(fr1)
ent2.insert(0,"1")
ent2.grid(row = 4,column = 1)

connect_bt = tk.Button(fr1,text = "Conectar",command = connect)
connect_bt.grid(row = 5,column = 0)

desconnect_bt = tk.Button(fr1,text = "Desconectar",command = desconnect)
desconnect_bt.grid(row = 5,column = 1)

send_bt = tk.Button(fr2,text = "Enviar múltiplos hex (xx-xx-xx-...)",command = send)
send_bt.grid(row = 6,column = 0)
hex_in = tk.Entry(fr2)
hex_in.grid(row = 6,column = 1)

rec_bt = tk.Button(fr2,text = "Receber hex",command = rec)
rec_bt.grid(row = 7,column = 0)
hex_out = tk.Entry(fr2)
hex_out.grid(row = 7,column = 1)

tx6 = tk.Label(fr3,text = "Frequênica inicial (Hz)")
tx6.grid(row = 0,column = 0)
ent3 = tk.Entry(fr3)
ent3.grid(row = 0,column = 1)

tx7 = tk.Label(fr3,text = "Frequênica final (Hz)")
tx7.grid(row = 1,column = 0)
ent4 = tk.Entry(fr3)
ent4.grid(row = 1,column = 1)

tx8 = tk.Label(fr3,text = "Número de pontos")
tx8.grid(row = 2,column = 0)
ent5 = tk.Entry(fr3)
ent5.grid(row = 2,column = 1)

plot_bt = tk.Button(fr3,text = "Plotar",command = plotar)
plot_bt.grid(row = 3,column = 0)

canvas = FigureCanvasTkAgg(fig,master = root)
canvas.get_tk_widget().grid(row = 0,column = 1)


root.mainloop()


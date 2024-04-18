import serial
import serial.tools.list_ports
import tkinter as tk

def connect():
    print("conectando...")
    global connection
    if connection.is_open: return
    
    selected = selected_port.get().split(":")
    port_name = selected[0]
    connection.port = port_name
    
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

    connection.timeout = float(ent3.get())


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

#interface
tx1 = tk.Label(root,text = "Porta")
tx1.grid(row = 0,column = 0)
menu_ports = tk.OptionMenu(root, selected_port,*port_options)
menu_ports.grid(row = 0,column = 1)

tx2 = tk.Label(root,text = "Baudrate (bits por segundo)")
tx2.grid(row = 1,column = 0)
ent1 = tk.Entry(root)
ent1.insert(0,"9600")
ent1.grid(row = 1,column = 1)

tx5 = tk.Label(root, text = "Paridade")
tx5.grid(row = 2,column = 0)
menu_parity = tk.OptionMenu(root,selected_parity,*parity_options)
menu_parity.grid(row = 2,column = 1)

tx3 = tk.Label(root,text = "Stop Bits")
tx3.grid(row = 3,column = 0)
menu_stopbits = tk.OptionMenu(root,selected_stopbits,*stopbits_options)
menu_stopbits.grid(row = 3,column = 1)

tx4 = tk.Label(root,text = "Timeout (segundos)")
tx4.grid(row = 4,column = 0)
ent3 = tk.Entry(root)
ent3.insert(0,"1")
ent3.grid(row = 4,column = 1)

connect_bt = tk.Button(root,text = "Conectar",command = connect)
connect_bt.grid(row = 5,column = 0)

desconnect_bt = tk.Button(root,text = "Desconectar")
desconnect_bt.grid(row = 5,column = 1)
root.mainloop()

"""
serial_port = '/dev/ttyACM0' # Porta
baud_rate = 115200  # Taxa
ser = serial.Serial(serial_port, baud_rate, timeout=1)
"""

import serial
import serial.tools.list_ports
import tkinter as tk

root = tk.Tk()
#variáveis
list_ports = []
ports = serial.tools.list_ports.comports()
if len(ports) > 0:
    list_ports = [i.name + ": " + i.manufacturer for i in ports]
else:
    list_ports.append("Sem portas")
selected_port = tk.StringVar()
selected_port.set(list_ports[0])
#interface
tx1 = tk.Label(root,text = "Porta")
tx1.grid(row = 0,column = 0)
menu = tk.OptionMenu(root, selected_port,*list_ports)
menu.grid(row = 0,column = 1)
tx2 = tk.Label(root,text = "Baudrate (bits por segundo)")
tx2.grid(row = 1,column = 0)
ent1 = tk.Entry(root)
ent1.grid(row = 1,column = 1)
ck_button = tk.Checkbutton(root, text = "Paridade")
ck_button.grid(row = 2,column = 0)
tx3 = tk.Label(root,text = "Stop Bits")
tx3.grid(row = 3,column = 0)
ent2 = tk.Entry(root)
ent2.grid(row = 3,column = 1)
tx4 = tk.Label(root,text = "Timeout (segundos)")
tx4.grid(row = 4,column = 0)
ent3 = tk.Entry(root)
ent3.grid(row = 4,column = 1)
connect_bt = tk.Button(root,text = "Conectar")
connect_bt.grid(row = 5,column = 0)
desconnect_bt = tk.Button(root,text = "Desconectar")
desconnect_bt.grid(row = 5,column = 1)
root.mainloop()

"""
serial_port = '/dev/ttyACM0' # Porta
baud_rate = 115200  # Taxa
ser = serial.Serial(serial_port, baud_rate, timeout=1)
"""

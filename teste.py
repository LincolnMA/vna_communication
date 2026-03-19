import serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

con = serial.Serial()
con.port = 'COM8'
con.baudrate = 115200
con.stopbits = 1

con.open()

con.write(b'\x0d')

response = con.read(1)
print(response)
    

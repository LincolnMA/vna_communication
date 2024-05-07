import serial
import time

a = serial.Serial(port = "/dev/ttyACM0", baudrate = 9600,timeout=1)
time.sleep(1.75)
a.write(bytearray(b'#\x00\x00\xca\x9a;\x00\x00\x00\x00#\x10\x00\xca\x9a;\x00\x00\x00\x00! \x02\x00!"\x01\x00\x180\x02'))
a.flush()
b = a.read(64)
print(b)
print(len(b))
a.close()
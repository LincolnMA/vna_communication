import serial

def send_hex_command(hex_command):
    # Define porta serial
    serial_port = '/dev/ttyACM0' # Porta
    baud_rate = 115200  # Taxa

    # Abrir porta Serial
    ser = serial.Serial(serial_port, baud_rate, timeout=1)

    try:
        # Enviar comando Hexa
        ser.write(bytes.fromhex(hex_command))
        print(f"Sent hexadecimal command: {hex_command}")

        # ler até 1024 bytes
        response = ser.read(1024)  # Read up to 1024 bytes of response
        print("Response:", response)

    except serial.SerialException as e:
        print("Error:", e)

    finally:
        # fechar porta
        ser.close()

if _name_ == "_main_":
    # Conforme o manual, enviando 0D o dispositivo retorna b'2' isso funciona
    hex_command_to_send = '0D'

    # enviar comando
    send_hex_command(hex_command_to_send)

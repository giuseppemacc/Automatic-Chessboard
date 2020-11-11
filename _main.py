import bluetooth
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

print("In attesa di una connessione")
client_sock,address = server_sock.accept()

ser.write(b"BT")
print("Connessione accetata da: ",address)
try:
    while True:
        #recv = client_sock.recv(1024)
        #print("input: ",recv)

        serial_value = str(ser.readline())[2:-1]
        print(serial_value)

        if serial_value == str("SHOOT"):
            print("SHHOOOUTOOOOOO")

        #send = input()
        #client_sock.send(str(send))

except:
    ser.write(b"BF")
    print("Connessione scaduta")
    client_sock.close()
    server_sock.close()
    ser.close()

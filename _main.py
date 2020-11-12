import bluetooth
import serial
from kivy.clock import Clock

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

print("In attesa di una connessione")
client_sock,address = server_sock.accept()

ser.write(b"BT")
print("Connessione accetata da: ",address)
Clock.schedule_interval(serial_flow,1)
try:
    while True:
        #recv = client_sock.recv(1024)
        #print("input: ",recv)
        #send = input()
        #client_sock.send(str(send))
        print("")

except:
    ser.write(b"BF")
    print("Connessione scaduta")
    client_sock.close()
    server_sock.close()
    ser.close()

def serial_flow(dt):
    serial_value = str(ser.readline())[2:-1]
    if serial_value == str("SHOOT"):
        print("SHOOT------------------------------------------------------------")
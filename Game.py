import bluetooth
import serial
import asyncio

class Game():
    def __init__(self):
        self.ser_arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.server_sock.bind(("",1))
        self.server_sock.listen(1)

        print("In attesa di una connessione")
        self.client_sock,self.address = self.server_sock.accept()

        self.ser_arduino.write(b"BT")
        print("Connessione accetata da: ",self.address)

    async def ser_io(self):
        while True:
            await asyncio.sleep(1)
            print("1")
            serial_value = str(self.ser_arduino.readline())[2:-1]
            if serial_value == "SHOOT":
                print("SHOOT")


    async def ble_io(self):
        while True:
            await asyncio.sleep(3)
            print("3")
            try:
                recv = self.client_sock.recv(1024)
                print("input: ",recv)
            except:
                self.ser_arduino.write(b"BF")
                print("Connessione scaduta")
                self.client_sock.close()
                self.server_sock.close()

    def stop(self):
        self.ser_arduino.close()
        self.client_sock.close()
        self.server_sock.close()


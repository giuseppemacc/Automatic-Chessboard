import bluetooth
import serial
import asyncio
import concurrent
import time
from os import system

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

    def get_ble_val(self):
        return self.client_sock.recv(1024)

    def get_ser_val(self):
        return str(self.ser_arduino.readline())[2:-1]


    async def ser_io(self):
        while True:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            loop = asyncio.get_event_loop()
            ser_val = await loop.run_in_executor(executor, self.get_ser_val)
            if ser_val == "SHOOT":
                print("SHOOT")
            elif ser_val == "SHUTDOWN":
                print("Spegnimento...")
                self.stop()
                time.sleep(5)
                system("shutdown now")

    async def ble_io(self):
        while True:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            loop = asyncio.get_event_loop()
            try:
                recv = await loop.run_in_executor(executor, self.get_ble_val)
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


import bluetooth
import serial
import asyncio
import concurrent
import time
from os import system


class Connection():
    def __init__(self):
        # variabili di connessione
        self.ser_arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        self.server_sock.bind(("",1))
        self.server_sock.listen(1)

    def init_connection(self):
        print("In attesa di una connessione")
        self.client_sock,self.address = self.server_sock.accept()

        print("Connessione accetata da: ",self.address)
    
    def close_connection(self):
        try:
            self.ser_arduino.close()
        except:
            pass
        
        try:
            self.client_sock.close()
        except:
            pass

        try:
            self.server_sock.close()
        except:
            pass
    
    def reload(self):
        pass

    def do_on_serval(self,ser_val):
        pass
    def do_on_bleval(self, bleval):
        pass

    async def ser_io(self):
        while True:
            try:
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
                loop = asyncio.get_event_loop()
                ser_val = await loop.run_in_executor(executor, self.get_ser_val)
                self.do_on_serval(ser_val)
            except:
                self.reload()

    async def ble_io(self):
        while True:
            try:
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
                loop = asyncio.get_event_loop()
                ble_val = await loop.run_in_executor(executor, self.get_ble_val)
                self.do_on_bleval(ble_val)
            except:
                self.reload()


    # ===== Funzioni sync da rendere async ================
    def get_ble_val(self):
        return str(self.client_sock.recv(1024))[2:-5]

    def get_ser_val(self):
        return str(self.ser_arduino.readline())[2:-1]

    def send_ble(self,value):
        try:
            self.client_sock.send(value)
        except:
            self.reload()

    def send_ser(self,value):
        try:
            self.ser_arduino.write(value.encode())
        except:
            self.reload()
    # ====================================================

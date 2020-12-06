import bluetooth
import serial
import asyncio
import concurrent
import time
from os import system
from shoot import shoot

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

        self.ser_arduino.write(b"BT")
        print("Connessione accetata da: ",self.address)
    
    def close_connection(self):
        self.ser_arduino.write(b"BF")
        time.sleep(1)
        self.ser_arduino.close()
        self.client_sock.close()
        self.server_sock.close()
    
    def do_on_serval(self,ser_val):
        pass
    def do_on_bleval(self, bleval):
        pass

    async def ser_io(self):
        while True:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            loop = asyncio.get_event_loop()
            ser_val = await loop.run_in_executor(executor, self.get_ser_val)
            self.do_on_serval(ser_val)

    async def ble_io(self):
        while True:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
            loop = asyncio.get_event_loop()
            try:
                ble_val = await loop.run_in_executor(executor, self.get_ble_val)
                self.do_on_bleval(ble_val)
            except:
                self.ser_arduino.write(b"BF")
                print("Connessione scaduta")
                self.client_sock.close()
                self.server_sock.close()
        


    # ===== Funzioni sync da rendere async ================
    def get_ble_val(self):
        return str(self.client_sock.recv(1024))[2:-5]

    def get_ser_val(self):
        return str(self.ser_arduino.readline())[2:-1]

    def send_ble(self,value):
        self.client_sock.send(value)
    
    def send_ser(self,value):
        self.ser_arduino.write(value)
    # ====================================================

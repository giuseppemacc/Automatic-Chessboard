from Connection import Connection
import time
from os import system

class Game(Connection):
    def __init__(self):
        super().__init__()
        self.init_connection()
    
    # @Override
    def do_on_serval(self, ser_val):
    
        if ser_val == "SHUTDOWN":
            print("Spegnimento...")
            time.sleep(5)
            quit()
            #system("shutdown now")
        elif ser_val == "SHOOT":
            print("SHOOT")
    
    # @Override
    def do_on_bleval(self, ble_val):
        print(ble_val)
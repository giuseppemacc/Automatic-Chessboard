from Connection import Connection
from Chessboard import Chessboard
from ImageProcessing import get_dicbool_chessboard
from PIL import Image
import time
from os import system
from shoot import shoot

white = [126,110,84]
black = [27,27,27]
offset = {
    "top": 29,
    "bottom": 28,
    "left_int": 17,
    "right_int": 15,
    "left_ext": 3,
    "right_ext":3,
    "color": [10,10]
}

class Game(Connection):
    def __init__(self):
        super().__init__()
        self.init_connection()
        self.chessboard = Chessboard()
        self.shoot_OnServal = None # function
        self.a = 0
        self.b = 0

    # @Override
    def do_on_serval(self, ser_val):
        print(ser_val)

        if ser_val == "SHUTDOWN":
            print("Spegnimento...")
            time.sleep(5)
            quit()
            #system("shutdown now")
        elif ser_val == "SHOOT":
            if not(self.shoot_OnServal == None):
                self.shoot_OnServal()
    
    # @Override
    def do_on_bleval(self, ble_val):
        print(ble_val)

        if ble_val == "GPFREE":
            self.shoot_OnServal = self.PosizionamentoLibero
    
    def PosizionamentoLibero(self):
        # scatta l'immagine
        # boolizza
        # fa see_move
        # modificare scacchiera
        # inviare la scacchiera tramite ble
        
        # shoot()
        # dicbool_chessboard = get_dicbool_chessboard(Image.open("image/shoot.jpg").resize((500,375)), offset, [white,black] )

        # print(dicbool_chessboard["grid"])

        # time.sleep(0.5)

        # move = self.chessboard.see_move(dicbool_chessboard)
        # # TODO: si verifica un bug che bho non lo so; da provare con il giusto setup iniziale delle pedine
        # self.chessboard.move(move)
        # print(self.chessboard)
        self.send_ble_Chessboard()

    def send_ble_Chessboard(self):
        # TODO: capire perch+ inviando questo ("//CB-0-0-wK\r\n") la pedina wK non viene riconosciuta e mette uno spazio bianco
        print(self.a,"    ",self.b)
        self.send_ble(f"CB-{self.a}-{self.b}-bk")
        
        if self.b >= 7:
            self.b = 0
            self.a += 1
        else:
            self.b +=1

        if self.a > 7:
            self.a = 0

        

        

        

        

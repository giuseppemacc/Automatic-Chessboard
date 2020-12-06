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
        self.ser_val_SHOOT = None 

    # @Override
    def do_on_serval(self, ser_val):
        print(ser_val)

        if ser_val == "SHUTDOWN":
            print("Spegnimento...")
            time.sleep(5)
            quit()
            #system("shutdown now")
        elif ser_val == "SHOOT":
            if not(self.ser_val_SHOOT == None):
                self.ser_val_SHOOT()
    
    # @Override
    def do_on_bleval(self, ble_val):
        print(ble_val)

        if ble_val == "GP-FREE":
            self.ser_val_SHOOT = self.PosizionamentoLibero
    
    def PosizionamentoLibero(self):
        # deve scattare l'immagine
        # boolizzarla
        # fare see_move
        # modificare scacchiera
        # inviare la scacchiera tramite ble
        
        shoot()
        dicbool_chessboard = get_dicbool_chessboard(Image.open("image/shoot.jpg").resize((500,375)), offset, [white,black] )

        print(dicbool_chessboard["grid"])

        time.sleep(0.5)

        move = self.chessboard.see_move(dicbool_chessboard)
        self.chessboard.move(move)
        print(self.chessboard)

        

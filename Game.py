from Connection import Connection
from Chessboard import Chessboard
from ImageProcessing import get_dicbool_chessboard
from PIL import Image
import time
from os import system
from shoot import shoot

white = [68,65,30]
black = [11,13,8]
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
            self.send_ble_Chessboard(all_chessboard=True)
            if not(self.shoot_OnServal == None):
                self.shoot_OnServal()
    
    # @Override
    def do_on_bleval(self, ble_val):
        print(ble_val)

        if ble_val == "GPFREE":
            self.shoot_OnServal = self.send_ble_Chessboard#self.PosizionamentoLibero
    
    def PosizionamentoLibero(self):
        # scatta l'immagine
        # boolizza
        # fa see_move
        # modificare scacchiera
        # inviare la scacchiera tramite ble
        
        shoot()
        dicbool_chessboard = get_dicbool_chessboard(Image.open("image/shoot.jpg").resize((500,375)), offset, [white,black] )

        print("New Chessboard:")
        print("")
        print(dicbool_chessboard["grid"])
        print("")
        print(dicbool_chessboard["bpn"])
        print("")
        print(dicbool_chessboard["wpn"])

        time.sleep(0.5)

        move = self.chessboard.see_move(dicbool_chessboard)
        print(move)
        self.chessboard.move(move)
        print(self.chessboard)
        #self.send_ble_Chessboard()

    def send_ble_Chessboard(self, string_type="", x=0, y=0, piece="", all_chessboard = False):
        if all_chessboard == True:
            for _x in range(8):
                for _y in range(8):
                    piece = self.chessboard.chessboard["grid"][_y][_x]
                    if piece == "░░" or piece == "██":
                        print("yes")
                        piece = "xx"
                    self.send_ble(f"CB-grid-{_y}-{_x}-{piece}")
                    time.sleep(0.5)
            for _y in range(2):
                for _x in range(8):
                    piece = self.chessboard.chessboard["bpn"][_y][_x]
                    if piece == "░░" or piece == "██":
                        piece = "xx"
                    self.send_ble(f"CB-bpn-{_y}-{_x}-{piece}")
                    time.sleep(0.5)
            for _y in range(2):
                for _x in range(8):
                    piece = self.chessboard.chessboard["wpn"][_y][_x]
                    if piece == "░░" or piece == "██":
                        piece = "xx"
                    self.send_ble(f"CB-wpn-{_y}-{_x}-{piece}")
                    time.sleep(0.5)
        else:
            self.send_ble(f"CB-{string_type}-{y}-{x}-{piece}")
            time.sleep(0.5)

        # print(self.a,"    ",self.b)
        # self.send_ble(f"CB-grid-{self.a}-{self.b}-bK")
        
        # if self.b >= 7:
        #     self.b = 0
        #     self.a += 1
        # else:
        #     self.b +=1

        # if self.a > 7:
        #     self.a = 0



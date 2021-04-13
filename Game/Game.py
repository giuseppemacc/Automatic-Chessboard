from Game.Connection import Connection
from Chessboard.Chessboard import Chessboard
from ImageProcesssing.ImageProcessing import binarizes, warpChessboard, cropImage
from PIL import Image
import time
from os import system
from ImageProcesssing.shoot import shoot

class Game(Connection):
    def __init__(self):
        super().__init__()
        self.init_connection()
        self.chessboard = Chessboard()
        self.initGame()
        self.shoot_OnServal = None # function


    # @Override
    def reload(self):
        # chiude le connessioni se ci sono e riavvia tutto
        self.close_connection()
        time.sleep(0.5)
        self.__init__()
        

    # @Override
    def do_on_serval(self, ser_val):
        if (ser_val != "") and (type(ser_val) == str):
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


    # Game functions
    
    def initGame(self):
        self.send_ble_Chessboard(all_chessboard=True)
    
    def PosizionamentoLibero(self):
        
        # scatta l'immagine
        # binarizza
        # fa see_move
        # modificare scacchiera
        # inviare la scacchiera tramite ble
        
        shoot()
        dicbool_chessboard = self.see_Chessboard()

        print("New Chessboard:")
        print("")
        print(dicbool_chessboard["grid"])
        print("")
        print(dicbool_chessboard["bpn"])
        print("")
        print(dicbool_chessboard["wpn"])

        # time.sleep(0.5)

        # move = self.chessboard.see_move(dicbool_chessboard)
        # print(move)
        # self.chessboard.move(move)
        # print(self.chessboard)

        #self.send_ble_Chessboard()

    def send_ble_Chessboard(self, string_type="", x=0, y=0, piece="", all_chessboard = False):
        if all_chessboard == True:
            for _y in range(8):
                for _x in range(8):
                    piece = self.chessboard.chessboard["grid"][_y][_x]
                    if piece == "░░" or piece == "██":
                        piece = "xx"
                    self.send_ble(f"CB-grid-{_y}-{_x}-{piece}")
                    time.sleep(0.01)

            for _y in range(2):
                for _x in range(8):
                    piece = self.chessboard.chessboard["bpn"][_y][_x]
                    if piece == "░░" or piece == "██":
                        piece = "xx"
                    self.send_ble(f"CB-bpn-{_y}-{_x}-{piece}")
                    time.sleep(0.01)

            for _y in range(2):
                for _x in range(8):
                    piece = self.chessboard.chessboard["wpn"][_y][_x]
                    if piece == "░░" or piece == "██":
                        piece = "xx"
                    self.send_ble(f"CB-wpn-{_y}-{_x}-{piece}")
                    time.sleep(0.01)

        else:
            self.send_ble(f"CB-{string_type}-{y}-{x}-{piece}")
            time.sleep(0.01)

    def see_Chessboard(self):
        warped_img = warpChessboard("shoot.jpg")
        crop_img = cropImage(warped_img)
        dic_bin_chessboard = binarizes(crop_img)

        return dic_bin_chessboard


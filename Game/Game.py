from Game.Connection import Connection
from Chessboard.Chessboard import Chessboard
from ImageProcessing.ImageProcessing import see_Chessboard
from ImageProcessing.shoot import shoot
import time
from os import system
import numpy as np

class Game(Connection):
    def __init__(self):
        super().__init__()
        self.init_connection()
        self.chessboard = Chessboard()
        
        self.shoot_OnServal = None # function
        self.flip_chessboard = False

        self.initGame()

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

        if ble_val == "PPFREE":
            self.shoot_OnServal = self.PosizionamentoLibero
        elif ble_val == "NG-W":
            self.shoot_OnServal = self.StandardGame
            self.flip_chessboard = False
        elif ble_val == "NG-B":
            # stockfish fa la prima mossa
            # viene ruotata fisicamente la scacchiera
            # bisogna ruotare la matrice della scacchiera già binarizzata
            # in questo modo è come se fosse tutto normale
            # poi quando bisogna far muovere il braccio bisogna calcolare la mossa invertendo la scacchiera
            self.flip_chessboard = True
            self.send_ble_Chessboard()

            move = self.chessboard.get_best_move()
            print(f"MOSSA fatta da Stockfish = {move}")
            arm_move = self.chessboard.move(move, arm_move=True)
            self.moveArm(arm_move)
            print(self.chessboard)
            self.send_ble_Chessboard()

            self.shoot_OnServal = self.StandardGame



    # Game functions
    
    def initGame(self):
        self.send_ble_Chessboard()


    def StandardGame(self):
        shoot()
        dicbool_chessboard = see_Chessboard()
        if self.flip_chessboard:
            # inverto grid
            # inverto lef e right
            # e poi left diventa right, e right diventa left
            dicbool_chessboard["grid"] = np.rot90(dicbool_chessboard["grid"], 2)
            temp = np.rot90(dicbool_chessboard["right"], 2)
            dicbool_chessboard["right"] = np.rot90(dicbool_chessboard["left"], 2)
            dicbool_chessboard["left"] = temp
            print(dicbool_chessboard)

        move = self.chessboard.see_move(dicbool_chessboard)
        print(f"MOSSA fatta dal giocatore = {move}")
        if (move != None) and (self.chessboard.stockfish.is_move_correct(move)):
            self.chessboard.move(move)
            print(self.chessboard)
            self.send_ble_Chessboard()
        
            move = self.chessboard.get_best_move()
            print(f"MOSSA fatta da Stockfish = {move}")
            arm_move = self.chessboard.move(move, arm_move=True)
            self.moveArm(arm_move)
            print(self.chessboard)
            
            self.send_ble_Chessboard()
        else:
            print("Mossa Non Valida")
            #self.send_ser("")
        
        self.send_ble_Chessboard()

    def PosizionamentoLibero(self):
        shoot()
        dicbin_chessboard = see_Chessboard()
        self.chessboard.see_move(dicbin_chessboard, free_pos=True)
        
        print(self.chessboard)
        self.send_ble_Chessboard()
    

    def moveArm(self, arm_move):

        for move in arm_move:
            print(move)
            if self.flip_chessboard:
                #M-100-100-P
                start_cord, end_cord, piece = move.split("-")[1:]
                type1,y1,x1 = start_cord
                type2,y2,x2 = end_cord
                type1 = int(type1)
                type2 = int(type2)
                y1 = 7 - int(y1)
                y2 = 7 - int(y2)
                x1 = int(x1)
                x2 = int(x2)


                if type1==1:
                    x1 = 7-x1
                else:
                    x1 = 1-x1

                if type2==1:
                    x2 = 7-x2
                else:
                    x2 = 1-x2

                if type1 == 0:
                    type1 = 2
                if type2 == 2:
                    type2 = 0

                move = f"M-{type1}{y1}{x1}-{type2}{y2}{x2}-{piece}"
                print(move)

            self.send_ser(move)

    def send_ble_Chessboard(self):
        board = {
            "left":self.chessboard.chessboard["left"],
            "grid":self.chessboard.chessboard["grid"],
            "right":self.chessboard.chessboard["right"]
        }
        if self.flip_chessboard:
            board["grid"] = np.rot90(board["grid"], 2)
            temp = np.rot90(board["right"], 2)
            board["right"] = np.rot90(board["left"], 2)
            board["left"] = temp
        
        print(self.chessboard)

        #CB-LEFT-00P-001R...-RIGHT-O1K...-GRID-80N
        string = "CB"

        string += "-LEFT"
        for y in range(8):
            for x in range(2):
                piece = board["left"][y][x]
                if piece == " ":
                    piece = "xx"
                elif piece.isupper():
                    piece = "w"+piece
                else:
                    piece = "b"+piece
                string += "-" + f"{y}{x}" + piece

        string += "-RIGHT"
        for y in range(8):
            for x in range(2):
                piece = board["right"][y][x]
                if piece == " ":
                    piece = "xx"
                elif piece.isupper():
                    piece = "w"+piece
                else:
                    piece = "b"+piece
                string += "-" + f"{y}{x}" + piece

        string += "-GRID"
        for y in range(8):
            for x in range(8):
                piece = board["grid"][y][x]
                if piece == " ":
                    piece = "xx"
                elif piece.isupper():
                    piece = "w"+piece
                else:
                    piece = "b"+piece
                string += "-" + f"{y}{x}" + piece

        #print("bluetooth string chessboard:")
        #print(string)
        self.send_ble(string)


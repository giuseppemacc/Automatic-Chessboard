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
        elif ble_val == "NG-W":
            self.StandardGame("W")
        elif ble_val == "NG-B":
            self.StandardGame("B")



    # Game functions
    
    def initGame(self):
        self.send_ble_Chessboard()

    def StandardGame(self, pieces):
        shoot()
        dicbool_chessboard = see_Chessboard()

        move = self.chessboard.see_move(dicbool_chessboard)
        print(f"MOSSA fatta dal giocatore = {move}")
        self.chessboard.move(move, player_move=True)
        print(self.chessboard)
        self.send_ble_Chessboard()

        move = self.chessboard.get_best_move()
        print(f"MOSSA fatta da Stockfish = {move}")
        arm_move = self.chessboard.move(move, arm_move=True)
        self.moveArm(arm_move)
        print(self.chessboard)
        
        self.send_ble_Chessboard()
    
    def PosizionamentoLibero(self):
        shoot()
        dicbool_chessboard = see_Chessboard()

        move = self.chessboard.see_move(dicbool_chessboard)
        print(f"MOSSA fatta dal giocatore = {move}")
        self.chessboard.move(move, player_move=True)
        print(self.chessboard)
        self.send_ble_Chessboard()

        move = self.chessboard.get_best_move()
        print(f"MOSSA fatta da Stockfish = {move}")
        arm_move = self.chessboard.move(move, arm_move=True)
        self.moveArm(arm_move)
        print(self.chessboard)
        
        self.send_ble_Chessboard()

    def moveArm(self, arm_move):
        for move in arm_move:
            self.send_ser(move)

    def send_ble_Chessboard(self):
        #CB-LEFT-00P-001R...-RIGHT-O1K...-GRID-80N
        string = "CB"

        string += "-LEFT"
        for y in range(8):
            for x in range(2):
                piece = self.chessboard.chessboard["left"][y][x]
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
                piece = self.chessboard.chessboard["right"][y][x]
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
                piece = self.chessboard.chessboard["grid"][y][x]
                if piece == " ":
                    piece = "xx"
                elif piece.isupper():
                    piece = "w"+piece
                else:
                    piece = "b"+piece
                string += "-" + f"{y}{x}" + piece

        print("bluetooth string chessboard:")
        print(string)
        self.send_ble(string)


#from Chessboard.type.t_cord import t_cord
#from Chessboard.type.t_move import t_move
from type.t_cord import t_cord
#from type.t_move import t_move
import chess
import chess.engine

import numpy as np

class Chessboard():
    def __init__(self):
        """
            la scacchiera si suddivide in 3 parti:
                - left / blu / bianchi
                - right / rossi / neri
                - grid / griglia
            contenute nel dizionario chessboard
        """
        #self.stockfish = Stockfish("Chessboard/stockfish_20090216_x64")

        self.player = "w"
        self.castling = "-"
        self.en_passant = "-"
        self.half_move_counter = 0
        self.move_counter = 1

        self.fen_position = ""

        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish_20090216_x64.exe")
        self.board = chess.Board()


        

        self.chessboard = {
            # TODO aggiungere un inizializzazione di wpn e bpn da due file .txt
            "grid": [
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "], 
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "],
            ],
            "left": [
                ["N","P"],
                ["N","P"],
                ["B","P"],
                ["B","P"],
                ["R","P"],
                ["R","P"],
                ["Q","P"],
                ["K","P"],
            ],
            "right": [
                ["p","n"],
                ["p","n"],
                ["p","b"],
                ["p","b"],
                ["p","r"],
                ["p","r"],
                ["p","q"],
                ["p","k"],
            ]                             
        }

    def set_piece(self, cord, piece):
        cord_index_form = cord.get_index_form()
        string_type = cord_index_form[0]
        y,x = cord_index_form[1]

        if piece == None:
            piece = " "

        self.chessboard[string_type][y][x] = piece

    def get_piece(self, cord):
        cord_index_form = cord.get_index_form()
        string_type = cord_index_form[0]
        y,x = cord_index_form[1]

        return self.chessboard[string_type][y][x]

    def refresh_fen_position(self):
        # 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
        string = ""
        for y in range(8):
            count = 0
            for x in range(8):
                square = self.chessboard["grid"][y][x]
                if square == " ":
                    count += 1
                    if x == 7:
                        string += str(count)
                else:
                    if count !=0:
                        string += str(count) + square
                        count = 0
                    else:
                        string += square
            if y != 7:
                string += "/"

        string += f" {self.player} {self.castling} {self.en_passant} {self.half_move_counter} {self.move_counter}"

        self.fen_position = string
        self.board = chess.Board(self.fen_position)

    def board_byfen_postion(self, fen_position):
        fen_list = fen_position.split("/")
        temp = fen_list[-1].split(" ")
        fen_list[-1] = temp[0]

        self.player = temp[1]
        self.castling = temp[2]
        self.en_passant = temp[3]
        self.half_move_counter = int(temp[4])
        self.move = int(temp[5])

        print(fen_list)

        for y in range(8):
            count = 0
            for x in range(len(fen_list[y])):
                char = fen_list[y][x]
                if char.isnumeric():
                    for i in range(int(char)):
                        self.chessboard["grid"][y][x+i] = " "
                else:
                    self.chessboard["grid"][y][x] = char
                
    def get_best_move(self):
        self.refresh_fen_position()
        
        move = str(engine.play(self.board, chess.engine.Limit(time=2.0)).move)
        print(move)


    def move(self, move):
        pass
    
    def see_move(self, dicbool):
        def is_notEmpty(a):
            if a == " ":
                return 0
            elif a.isupper():
                return 1
            else:
                return 2
                

        bool_current_chessboard = {
            "left": [ [is_notEmpty(j) for j in i] for i in self.chessboard["left"]],
            "right": [ [is_notEmpty(j) for j in i] for i in self.chessboard["right"]],
            "grid": [ [is_notEmpty(j) for j in i] for i in self.chessboard["grid"]],
        }

        def compare(first, second):
            if first == second:
                return first
            else:
                if second == 0:
                    return "-"
                elif first == 0:
                    return "+"
                else:
                    return "/"
                 
        bool_new_chessboard = {
            "left":  [ [compare(bool_current_chessboard["left"][i][j], dicbool["left"][i][j]) for j in range(2)] for i in range(8)],
            "right":  [ [compare(bool_current_chessboard["right"][i][j], dicbool["right"][i][j]) for j in range(2)] for i in range(8)],
            "grid": [ [compare(bool_current_chessboard["grid"][i][j], dicbool["grid"][i][j]) for j in range(8)] for i in range(8)]
        }

        changes = {
            "+":[],
            "-":[],
            "/":[]
        }

        def count_changes(string_type):
            for y in range(len( bool_new_chessboard[string_type] )):
                for x in range(len( bool_new_chessboard[string_type][y] )):

                    if bool_new_chessboard[string_type][y][x] == "-":
                        changes["-"].append( t_cord(index_form = [string_type,[y,x]]) )

                    elif bool_new_chessboard[string_type][y][x] == "+":
                        changes["+"].append( t_cord(index_form = [string_type,[y,x]]) )

                    elif bool_new_chessboard[string_type][y][x] == "/":
                        changes["/"].append( t_cord(index_form = [string_type,[y,x]]) )
        
        count_changes("left")
        count_changes("right")
        count_changes("grid") 

        # caso di una mossa normale
        if (len(changes["+"])==1 and len(changes["-"])==1 and len(changes["/"])==0 ):
            piece = self.get_piece( changes["-"][0] )
            self.set_piece( changes["-"][0], None )
            self.set_piece( changes["+"][0], piece )

        elif (len(changes["+"])==1 and len(changes["-"])==1 and len(changes["/"])==1 ):
            
            pusher_piece = self.get_piece( changes["-"][0] )
            pushed_piece = self.get_piece( changes["/"][0] )

            self.set_piece( changes["-"][0], None )
            self.set_piece( changes["/"][0], pusher_piece )
            self.set_piece( changes["+"][0], pushed_piece )

        print(np.array(bool_new_chessboard["left"]))
        print(np.array(bool_new_chessboard["grid"]))
        print(np.array(bool_new_chessboard["right"]))

        #print(changes["+"][0].get_index_form())
        #print(changes["-"][0].get_index_form())
        #print(changes["/"][0].get_index_form())

        
    def __str__(self):
        string = "==================\n"
        string += str(np.array(self.chessboard["left"]))
        string += "\n==================\n"
        string += str(np.array(self.chessboard["grid"]))
        string += "\n==================\n"
        string += str(np.array(self.chessboard["right"]))
        string += "\n==================\n"

        return string

if __name__ == '__main__':
    """
    esempio di utilizzo
    """
    chessboard = Chessboard()

    # dicbool = {
        # "left" : np.full((8,2), 1),
        # "right" : np.full((8,2), 2),
        # "grid" : np.full((8,8), 0)
    # }
# 
    # dicbool["left"][0][0] = 2
    # dicbool["right"][0][0] = 0
    # dicbool["grid"][0][0] = 1
# 
    # chessboard.see_move(dicbool)
# 
    # chessboard.refresh_fen_position()
# 
    #print(chessboard)
    # print(chessboard.fen_position)

    chessboard.board_byfen_postion('rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1')
    print(chessboard)

    #chessboard.move(t_move(string_form="wK-la1-e4"))
    #print(chessboard)

    # dicbool = {
    #     "wpn" : np.full((2,8), True),
    #     "bpn" : np.full((2,8), True),
    #     "grid" : np.full((8,8), False)
    # }
    # dicbool["wpn"][0][4] = False
    # dicbool["grid"][3][5] = True

    # print(chessboard)
    # chessboard.see_move(dicbool)
    # print(chessboard)
    #print(chessboard)
    #chessboard.see_move(dicbool)
    #chessboard.move(t_move("bK-bpnb2-e8"))
    #chessboard.move(t_move("bR-bpnc1-a8"))
    #chessboard.move(t_move("wK-wpnb2-e1"))
    #chessboard.move(t_move("wR-wpnc1-h1"))
    #chessboard.move(t_move("bR-bpnc2-h8"))
    #chessboard.move(t_move("wR-bpnc2-a1"))
    #chessboard.move(t_move("bO-O"))
    #chessboard.move(t_move("wO-O-O"))
    #cord = t_cord(cord_numeric=["wpn",[0,4]])
    #print(cord)
    #print(cord.get_numeric())
    #chessboard.set(cord, "wV")
    #print(chessboard)
    #print(chessboard.get(cord_numeric=["wpn",[0,4]]))
    #print(chessboard.get(cord=cord))
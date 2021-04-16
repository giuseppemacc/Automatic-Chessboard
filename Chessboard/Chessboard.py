from Chessboard.type.t_cord import t_cord
#from Chessboard.type.t_move import t_move
#from type.t_cord import t_cord
#from type.t_move import t_move
from stockfish import Stockfish

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

        self.castling = "-"
        self.en_passant = "-"
        self.half_move_counter = 0
        self.move_counter = 0

        self.fen_position = ""


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

    def get_fen_position(self):
        pass

    def get_best_move(self):
        pass
        # get_fen_position
        # poi in base alla fen position ricavata la mossa migliore
        # ritorna la mossa

    def move(self, move):
        piece, start_cord, end_cord, types = move.get_cord_form()

        if "castling_short" in types:
            if "black" in types:
                self.set(t_cord("e8"),None)
                self.set(t_cord("g8"),"bK")
                self.set(t_cord("h8"),None)
                self.set(t_cord("f8"),"bR")
            else:
                self.set(t_cord("e1"),None)
                self.set(t_cord("g1"),"wK")
                self.set(t_cord("h1"),None)
                self.set(t_cord("f1"),"wR")
        elif "castling_long" in types:
            if "black" in types:
                self.set(t_cord("e8"),None)
                self.set(t_cord("c8"),"bK")
                self.set(t_cord("a8"),None)
                self.set(t_cord("d8"),"bR")
            else:
                self.set(t_cord("e1"),None)
                self.set(t_cord("c1"),"wK")
                self.set(t_cord("a1"),None)
                self.set(t_cord("d1"),"wR")
        else:
            self.set(start_cord,None)
            self.set(end_cord,piece)

            if "en_passant" in types:
                x,y = end_cord.get_index_form()[1]

                if "black" in types:
                    self.set(t_cord(index_form=["grid",[x,y-1]]), None)
                elif "white" in types:
                    self.set(t_cord(index_form=["grid",[x,y+1]]), None)
    
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

        print(changes["+"][0].get_index_form())
        print(changes["-"][0].get_index_form())
        print(changes["/"][0].get_index_form())

        
    def __str__(self):
        string = "==================\n"
        for i in self.chessboard["left"]:
            for j in i:
                string += j
            string += "\n"
        string += "==================\n"

        count = 8
        for i in self.chessboard["grid"]:
            string += str(count)
            for j in i:
                string += j
            string += "\n"
            count -= 1

        string += " a b c d e f g h\n"
        string += "==================\n"
        for i in self.chessboard["right"]:
            for j in i:
                string += j
            string += "\n"
        string += "==================\n"
        
        return string

if __name__ == '__main__':
    """
    esempio di utilizzo
    """
    chessboard = Chessboard()

    dicbool = {
        "left" : np.full((8,2), 1),
        "right" : np.full((8,2), 2),
        "grid" : np.full((8,8), 0)
    }

    dicbool["left"][0][0] = 2
    dicbool["right"][0][0] = 0
    dicbool["grid"][0][0] = 1

    chessboard.see_move(dicbool)

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
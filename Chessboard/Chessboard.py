from Chessboard.t_cord import t_cord
import stockfish
import chess


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
        self.vatange = 0.5
        self.player = "w"
        self.castling = "KQkq"
        self.en_passant = "-"
        self.half_move_counter = 0
        self.move_counter = 1

        self.fen_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        self.stockfish = stockfish.Stockfish("./Chessboard/stockfish")
        self.stockfish.set_skill_level(1)
        self.board = chess.Board(self.fen_position)

        self.chessboard = {
            # TODO aggiungere un inizializzazione di wpn e bpn da due file .txt
            "grid": [
                ["r","n","b","q","k","b","n","r"],
                ["p","p","p","p","p","p","p","p"],
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "], 
                [" "," "," "," "," "," "," "," "],
                [" "," "," "," "," "," "," "," "],
                ["P","P","P","P","P","P","P","P"],
                ["R","N","B","Q","K","B","N","R"],
            ],
            "left": [
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
            ],
            "right": [
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
                [" "," "],
            ]                             
        }

    def get_vantage(self):
        # dove c'è il - è il vantaggio del nero
        # tipi:
        # "type": "cp", "value": -num/num
        # "type": "mate", "value": -1/1
        vantage = 0
        info = self.stockfish.get_evaluation()
        value = info["value"]
        if info["type"] == "mate":
            if value<0:
                vantage = 0
            else:
                vantage = 100
        elif info["type"] == "cp":
            vantage = (5+(value/100))*10
            if vantage>100:
                vantage = 100
            elif vantage<0:
                vantage = 0
        return int(vantage)

    def is_checkmate(self):
        self.refresh_fen_position()
        self.board.set_fen(self.fen_position)

        return (self.board.is_stalemate() or self.board.is_checkmate() or self.board.is_insufficient_material())

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

    def isValid_move(self,move):
        return (move != None) and (self.stockfish.is_move_correct(move))

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
        self.stockfish.set_fen_position(self.fen_position)
                
    def get_best_move(self):
        return self.stockfish.get_best_move_time(5000)

    def cord_piece_default(self, piece):
        cord = t_cord()

        if piece.isupper():
            if piece == "P":
                y = 0
                while self.get_piece(t_cord(index_form=["left",[y,1]])) != " ":
                    y+=1
                cord = t_cord(index_form=["left",[y,1]])

            elif piece == "N":
                y = 0
                while self.get_piece(t_cord(index_form=["left",[y,0]])) != " ":
                    y+=1
                cord = t_cord(index_form=["left",[y,0]])
            elif piece == "B":
                y = 2
                while self.get_piece(t_cord(index_form=["left",[y,0]])) != " ":
                    y+=1
                cord = t_cord(index_form=["left",[y,0]])
            elif piece == "R":
                y = 4
                while self.get_piece(t_cord(index_form=["left",[y,0]])) != " ":
                    y+=1
                cord = t_cord(index_form=["left",[y,0]])
            elif piece == "Q":
                cord = t_cord(index_form=["left",[6,0]])
            elif piece == "K":
                cord = t_cord(index_form=["left",[7,0]])

        else:
            if piece == "p":
                y = 7
                while self.get_piece(t_cord(index_form=["right",[y,0]])) != " ":
                    y-=1
                cord = t_cord(index_form=["right",[y,0]])

            elif piece == "n":
                y = 7
                while self.get_piece(t_cord(index_form=["right",[y,1]])) != " ":
                    y-=1
                cord = t_cord(index_form=["right",[y,1]])
            elif piece == "b":
                y = 5
                while self.get_piece(t_cord(index_form=["right",[y,1]])) != " ":
                    y-=1
                cord = t_cord(index_form=["right",[y,1]])
            elif piece == "r":
                y = 3
                while self.get_piece(t_cord(index_form=["right",[y,1]])) != " ":
                    y-=1
                cord = t_cord(index_form=["right",[y,1]])
            elif piece == "q":
                cord = t_cord(index_form=["right",[1,1]])
            elif piece == "k":
                cord = t_cord(index_form=["right",[0,1]])

        return cord
        
    def change_player(self):
        if self.player == "w":
            self.player = "b"
        elif self.player == "b":
            self.player = "w"

    # partendo dalla mossa modifica la scacchiera
    def move(self, move=None, arm_move=False):

        # se termina con una lettera vuol dire che c'è la promozione
        # quindi bisogna cambiare start_piece

        moves_cord = []

        start_cord = t_cord(string_form = move[:2])
        end_cord = t_cord(string_form = move[2:4])

        index_start_cord = start_cord.get_index_form()
        index_end_cord = end_cord.get_index_form()

        start_piece = ""
        end_piece = self.get_piece(end_cord)
        
        # in caso di promozione
        if move[-1].isalpha():
            if self.player == "w":
                start_piece = move[-1].upper()
            else:    
                start_piece = move[-1]
        else:
            start_piece = self.get_piece(start_cord)

        # arrocco corto bianco
        if (move == "e1g1") and ("K" in self.castling):
            self.set_piece(t_cord(string_form="e1"),None)
            self.set_piece(t_cord(string_form="h1"),None)
            self.set_piece( t_cord(string_form="g1"), "K" )
            self.set_piece( t_cord(string_form="f1"), "R" )

            self.castling = self.castling.replace("K","")
            
            moves_cord.append("M-174-176-K")
            moves_cord.append("M-177-175-R")
        # arrocco lungo bianco
        elif move == "e1c1" and ("Q" in self.castling):
            self.set_piece(t_cord(string_form="e1"),None)
            self.set_piece(t_cord(string_form="a1"),None)
            self.set_piece( t_cord(string_form="c1"), "K" )
            self.set_piece( t_cord(string_form="d1"), "R" )

            self.castling = self.castling.replace("Q","")

            moves_cord.append("M-174-172-K")
            moves_cord.append("M-170-173-R")
        # arrocco corto nero
        elif move == "e8g8" and ("k" in self.castling):
            self.set_piece(t_cord(string_form="e8"),None)
            self.set_piece(t_cord(string_form="h8"),None)
            self.set_piece( t_cord(string_form="g8"), "k" )
            self.set_piece( t_cord(string_form="f8"), "r" )

            self.castling = self.castling.replace("k","")

            moves_cord.append("M-104-106-K")
            moves_cord.append("M-107-105-R")
        # arrocco lungo nero
        elif move == "e8c8" and ("q" in self.castling):
            self.set_piece(t_cord(string_form="e8"),None)
            self.set_piece(t_cord(string_form="a8"),None)
            self.set_piece( t_cord(string_form="c8"), "k" )
            self.set_piece( t_cord(string_form="d8"), "r" )

            self.castling = self.castling.replace("q","")

            moves_cord.append("M-104-102-K")
            moves_cord.append("M-100-103-R")
        # spostamento standard
        elif end_piece == " ":
            self.set_piece(start_cord, None)
            self.set_piece(end_cord, start_piece)

            moves_cord.append(f"M-1{index_start_cord[1][0]}{index_start_cord[1][1]}-1{index_end_cord[1][0]}{index_end_cord[1][1]}-{start_piece.upper()}")
        # cattura
        else:
            self.set_piece(start_cord, None)
            self.set_piece(end_cord, start_piece)

            if arm_move:
                cord_default = self.cord_piece_default(end_piece)
                self.set_piece(cord_default, end_piece)

                end_piece_defaul = cord_default.get_index_form()

                string_type = end_piece_defaul[0]
                y,x = end_piece_defaul[1]

                index_type = 1
                if string_type == "left":
                    index_type = 0

                moves_cord.append(f"M-1{index_end_cord[1][0]}{index_end_cord[1][1]}-{index_type}{y}{x}-{end_piece.upper()}")
                moves_cord.append(f"M-1{index_start_cord[1][0]}{index_start_cord[1][1]}-1{index_end_cord[1][0]}{index_end_cord[1][1]}-{start_piece.upper()}")

        self.change_player()
        self.refresh_fen_position()

        if arm_move:
            return moves_cord
            
    # partendo dall'immagine binarizzati ricava la mossa
    def see_move(self, dicbool, free_pos=False):
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

        move = None
        print("-----CAMBIAMENTI----")
        print(np.array(bool_new_chessboard["left"]))
        print(np.array(bool_new_chessboard["grid"]))
        print(np.array(bool_new_chessboard["right"]))
        print("\n")

        # spostamento standard
        if (len(changes["+"])==1 and len(changes["-"])==1 and len(changes["/"])==0 ):
            move = str(changes["-"][0].get_string_form()) + str(changes["+"][0].get_string_form())
            if free_pos:
                self.set_piece(changes["+"][0], self.get_piece(changes["-"][0]))
                self.set_piece(changes["-"][0], None)

        # cattura
        elif (len(changes["+"])==1 and len(changes["-"])==1 and len(changes["/"])==1 ):
            move = str(changes["-"][0].get_string_form()) + str(changes["/"][0].get_string_form())
            # setta qua il pezzo che va in panchina
            self.set_piece(changes["+"][0], self.get_piece(changes["/"][0]))

    
        elif (len(changes["+"])==2 and len(changes["-"])==2 and len(changes["/"])==0 ):
            cord_1, cord_2 = changes["+"]

            # arrocco corto bianco
            if ([cord_1.get_string_form(),cord_2.get_string_form()] == ["f1","g1"]) or ([cord_1.get_string_form(),cord_2.get_string_form()] == ["g1","f1"] ):
                move = "e1g1"   

            # arrocco lungo bianco
            elif ([cord_1.get_string_form(),cord_2.get_string_form()] == ["c1","d1"]) or ([cord_1.get_string_form(),cord_2.get_string_form()] == ["d1","c1"] ):
                move = "e1c1"

            # arrocco corto nero
            elif ([cord_1.get_string_form(),cord_2.get_string_form()] == ["f8","g8"]) or ([cord_1.get_string_form(),cord_2.get_string_form()] == ["g8","f8"] ):
                move = "e8g8"

            # arrocco lungo nero
            elif ([cord_1.get_string_form(),cord_2.get_string_form()] == ["c8","d8"]) or ([cord_1.get_string_form(),cord_2.get_string_form()] == ["d8","c8"] ):
                move = "e8c8"

        if not free_pos:
            start_piece = self.get_piece(t_cord(string_form=move[:2]))
            end_y = t_cord(string_form=move[2:]).get_index_form()[1][0]
            if start_piece == "P" and end_y == 0:
                move+="q" 
            elif start_piece == "p" and end_y == 7:
                move+="q" 

        return move

    def __str__(self):
        string = "==================\n"
        string += str(np.array(self.chessboard["right"]))
        string += "\n==================\n"
        string += str(np.array(self.chessboard["grid"]))
        string += "\n==================\n"
        string += str(np.array(self.chessboard["left"]))
        string += "\n==================\n"

        return string

if __name__ == '__main__':
    """
    esempio di utilizzo
    """
    chessboard = Chessboard()
    print(chessboard.cord_piece_default("P"))

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


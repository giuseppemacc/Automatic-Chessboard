from type.t_cord import t_cord
from type.t_move import t_move
import numpy as np

class Chessboard():
    def __init__(self):
        """
            la scacchiera si suddivide in 3 parti:\n
                - panchina nera (bpn)
                - panchina bianca (wpn)
                - griglia (grid)
            contenute nel dizionario chessboard
        """
        self.chessboard = {
            # TODO aggiungere un inizializzazione di wpn e bpn da due file .txt
            "wpn": [
                ["wQ","wK","wR","wB","wN","wP","wP","wP"],
                ["wQ","wQ","wR","wB","wN","wP","wP","wP"]
            ],
            "bpn": [
                ["bQ","bK","bR","bB","bN","bP","bP","bP"],
                ["bQ","bQ","bR","bB","bN","bP","bP","bP"]
            ],
            "grid": [
                ["██","░░","██","░░","██","░░","██","░░" ],
                ["░░","██","░░","██","░░","██","░░","██" ],
                ["██","░░","██","░░","██","░░","██","░░" ],
                ["░░","██","░░","██","░░","██","░░","██" ], #
                ["██","░░","██","░░","██","░░","██","░░" ],
                ["░░","██","░░","██","░░","██","░░","██" ],
                ["██","░░","██","░░","██","░░","██","░░" ],
                ["░░","██","░░","██","░░","██","░░","██" ],
            ]                              #
        }

    def move(self,move):
        type = move.get_type()
        piece = move.get_piece()
        dic_cord = move.get_start_end_cord()

        if "castling_short" in type:
            if "black" in type:
                self.set(t_cord("e8"),None)
                self.set(t_cord("g8"),"bK")
                self.set(t_cord("h8"),None)
                self.set(t_cord("f8"),"bR")
            else:
                self.set(t_cord("e1"),None)
                self.set(t_cord("g1"),"wK")
                self.set(t_cord("h1"),None)
                self.set(t_cord("f1"),"wR")
        elif "castling_long" in type:
            if "black" in type:
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
            self.set(dic_cord["start"],None)
            self.set(dic_cord["end"],piece)
            if "en_passant" in type:
                cord_end_str = dic_cord["end"].get_string()
                if "black" in type:
                    self.set(t_cord( cord_end_str[0] + str(int(cord_end_str[1])+1) ) ,None)
                else:
                    self.set(t_cord( cord_end_str[0] + str(int(cord_end_str[1])-1) ) ,None)

    def set(self, cord, piece):
        # TODO aggiungere qui la modifica vera e propria della scacchiera reale quindi una funzione che faccia muovere il braccio robotico
        str_cord = cord.get_string()
        y, x = cord.get_numeric()[1]  
        string = ""
        if "wpn" in str_cord:      
            if piece == None:
               string = "██"
            else:
               string = piece
            self.chessboard["wpn"][y][x] = string
        elif "bpn" in str_cord:
            if piece == None:
               string = "░░"
            else:
               string = piece
            self.chessboard["bpn"][y][x] = string
        else: 
            if piece == None:
                if (x % 2 == 0 and (y+7) % 2 == 0) or ((x-1) % 2 == 0 and ((y+7)-1) % 2 == 0):
                    string = "░░"
                else:
                    string = "██"
            else:
                string = piece

            self.chessboard["grid"][y][x] = string
    
    def get(self, cord=None, cord_numeric=None):
        # cord_numeric è nel formato ["wpn",[y,x]]
        if cord == None and cord_numeric == None:
            print("ERRORE parametro cord o cord_numeric mancante")
        if cord == None:
            cord = t_cord(cord_numeric=cord_numeric)

        cord_string = cord.get_string()
        y,x = cord.get_numeric()[1]


        if "bpn" in cord_string:
            return self.chessboard["bpn"][y][x]
        elif "wpn" in cord_string:
            return self.chessboard["wpn"][y][x]
        else:
            return self.chessboard["grid"][y][x]
    
    def see_move(self, dicbool):

        def is_notEmpty(a):
            if (a == "░░") or (a == "██"):
                return False
            else:
                return True

        bool_current_chessboard = {
            "wpn": [ [is_notEmpty(j) for j in i] for i in self.chessboard["wpn"]],
            "bpn": [ [is_notEmpty(j) for j in i] for i in self.chessboard["bpn"]],
            "grid": [ [is_notEmpty(j) for j in i] for i in self.chessboard["grid"]],
        }
        print("Old Chessboard:")
        print("")
        print(bool_current_chessboard["grid"])
        print("")
        print(bool_current_chessboard["bpn"])
        print("")
        print(bool_current_chessboard["wpn"])

        
        def compare(first, second):
            if first == second:
                return first
            elif first == True:
                return "-"
            else:
                return "+"
                
        bool_new_chessboard = {
            "wpn":  [ [compare(bool_current_chessboard["wpn"][i][j], dicbool["wpn"][i][j]) for j in range(8)] for i in range(2)],
            "bpn":  [ [compare(bool_current_chessboard["bpn"][i][j], dicbool["bpn"][i][j]) for j in range(8)] for i in range(2)],
            "grid": [ [compare(bool_current_chessboard["grid"][i][j], dicbool["grid"][i][j]) for j in range(8)] for i in range(8)]
        } # questo dic contiene il bool della nuova scacchiera CON DEI VALORI CAMBIATI:
          # dove in bool_current_chessboard vi era un True ed in dicbool vi è un False, ci sarà "-" (significa che la pedina è stata tolta)
          # dove in bool_current_chessboard vi era un False ed in dicbool vi è un True, ci sarà "+" (significa che la pedina è stata messa)
        
        changes = {
            "+":[],
            "-":[]
        } # questo dic contiene:
          # "-": una lista delle cordinate sritte in cord_numeric (["type",[y,x]]) dove è stata tolta una pedina
          # "+": una lista delle cordinate sritte in cord_numeric (["type",[y,x]]) dove è stata messa una pedina


        def count_changes(bool_chessboard, chessboard_type):
            for y in range(len(bool_chessboard)):
                for x in range(len(bool_chessboard[y])):
                    if bool_chessboard[y][x] == "-":
                        changes["-"].append([chessboard_type,[y,x]])
                    elif bool_chessboard[y][x] == "+":
                        changes["+"].append([chessboard_type,[y,x]])
        
        count_changes(bool_new_chessboard["wpn"],"wpn")
        count_changes(bool_new_chessboard["bpn"],"bpn")
        count_changes(bool_new_chessboard["grid"],"grid")

        move = None
        start_piece = ""
        end_piece = ""

        if (len(changes["+"])==1 and len(changes["-"])==1):

            start_piece = self.get(cord_numeric=changes["-"][0])
            end_piece = self.get(cord_numeric=changes["+"][0])

            start_cord = t_cord(cord_numeric=changes["-"][0])
            end_cord = t_cord(cord_numeric=changes["+"][0])

            #TODO: in base al tipo di mossa: taking, promotion modificare la mossa aggiungendo "x" o "="
            move = t_move(start_piece+"-"+start_cord.get_string()+"-"+end_cord.get_string())
            
        return move
        
    def __str__(self):
        string = "==================\n"
        for i in self.chessboard["bpn"]:
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
        for i in self.chessboard["wpn"]:
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
        "wpn" : np.full((2,8), True),
        "bpn" : np.full((2,8), True),
        "grid" : np.full((8,8), False)
    }
    dicbool["wpn"][0][4] = False
    dicbool["grid"][3][5] = True

    print(chessboard)
    chessboard.see_move(dicbool)
    print(chessboard)
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
#from  Chessboard.type.t_cord import t_cord
from type.t_cord import t_cord


# mi deve indentificare una mossa
#   cordinate inizio e fine
#   piece
#   eventuale tipo di mossa (promozione, arrocco, en_passant)
# mi deve poter definire le sotto mosse da fare per fare la mossa completa
class t_move():
    """
        cord_form = [ "piece", start_cord, end_cord, [types] ]
        string_form = "wK-a1-a2", "bK-ra1-a2", "a1e2"
        types: white, black, castling_short ecc...
    """
    def __init__(self, cord_form=None, string_form=None):
        self.cord_form = cord_form
        self.string_form = string_form

    def get_string_form(self):
        if self.string_form == None:
            self.string_form = self.cord_form[0] +"-"+ self.cord_form[1].get_string_form() +"-"+ self.cord_form[2].get_string_form()
            types = self.cord_form[3]

            if "en_passant" in types:
                self.string_form += "-"+ "e.p."

            if "promotion" in types:
                self.string_form += "-"+ "=Q"

            if "castling_short" in types:
                if "black" in types:
                    self.string_form += "bO-O"
                elif "white" in types:
                    if "black" in types:
                        self.string_form += "wO-O"

            if "castling_long" in types:
                if "black" in types:
                    self.string_form += "bO-O-O"
                elif "white" in types:
                    if "black" in types:
                        self.string_form += "wO-O-O"
        
        return self.string_form

    def get_cord_form(self):
        if self.cord_form == None:

            if "O" in self.string_form:
                if self.string_form[1:] == "O-O":
                    self.cord_form = [None,None,None,["castling_short"]]
                elif self.string_form[1:] == "O-O-O":
                    self.cord_form = [None,None,None,["castling_long"]]
                
                if self.string_form[0][0] == "w":
                    self.cord_form[-1].append("white")
                elif self.string_form[0][0] == "b":
                    self.cord_form[-1].append("black")
            else:

                splitted_string_form = self.string_form.split("-")
                piece, string_start_cord, string_end_cord = splitted_string_form[:3]
                self.cord_form = [piece, t_cord(string_start_cord), t_cord(string_end_cord)]

                types = []
                
                # verifica se la mossa è di tipo bianco o nero
                if piece[0] == "w":
                    types.append("white")
                elif piece[0] == "b":
                    types.append("black")


                if len(splitted_string_form) == 4:
                    type = splitted_string_form[3]
                    
                    if "=" in type:
                        types.append("promotion")
                    if "e.p." in type:
                        types.append("en_passant")
                
                self.cord_form.append(types)

        return self.cord_form


# class t_move():
#     """type of move:\n
#             - "white"
#             - "black"
#             - "castling_short"
#             - "castling_long"
#             - "taking"
#             - "promotion"
#             - "en_passant"
#         esempi di mosse:\n
#             - "bK-bpnb2-e8" (Re da panchina b2 a e8)
#             - "bK-e8-bpnb2" (Re da e8 a panchina b2)
#             - "bK-e8-f8" (Re da e8 a f8)
#             - "bO-O" oppure "wO-O-O" (arrocco corto e lungo)
#             - "bK-e8-x-f8" (Re da e8 mangia in f8)
#             - "wP-c7-c8-=wQ" (Pedone va a promozione da c7 a c8)
#             - "wP-c7-x-d8-=wQ" (Pedone va a promozione mangiando da c7 a d8)
#             - "wP-e5-x-e6-e.p." (Pedone mangia en passant da e5 a e6)
#     """
#     moves_counter = 0
#     def __init__(self, move_string):
#         self.move_string = move_string
#         t_move.moves_counter += 1

#     def get_type(self):
#         """
#         ritorna una lista di stringa contenente i tipi della mossa
#         es:\n
#             - ["white","promotion"]
#             - ["black","taking","en_passant"]
#         """
#         type = []

#         if self.move_string.startswith("b"):
#             type.append("black")
#         if self.move_string.startswith("w"):
#             type.append("white")
        
#         if self.move_string[1:] == "O-O" :
#             type.append("castling_short")
#         elif self.move_string[1:] == "O-O-O":
#             type.append("castling_long")
#         else:
#             if "x" in self.move_string:
#                 type.append("taking")
#             if "=" in self.move_string:
#                 type.append("promotion") 
#             if "." in self.move_string:
#                 type.append("en_passant")
#         return type
    
#     def get_start_end_cord(self):
#         cord = {
#             "start": None,
#             "end": None,
#         }
#         splitted_move = self.move_string.split("-")
#         if "O" in self.move_string:
#             pass
#         else:
#             cord["start"] = t_cord(splitted_move[1])
#             if "x" in self.move_string:
#                 cord["end"] = t_cord(splitted_move[3])
#             else:
#                 cord["end"] = t_cord(splitted_move[2])

        
#         return cord
    
#     def get_piece(self):
#         if "=" in self.move_string:
#             return self.move_string[-2:]
#         else:
#             return self.move_string[:2]
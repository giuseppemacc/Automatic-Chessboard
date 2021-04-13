from type.t_cord import t_cord

class t_move():
    """type of move:\n
            - "white"
            - "black"
            - "castling_short"
            - "castling_long"
            - "taking"
            - "promotion"
            - "en_passant"
        esempi di mosse:\n
            - "bK-bpnb2-e8" (Re da panchina b2 a e8)
            - "bK-e8-bpnb2" (Re da e8 a panchina b2)
            - "bK-e8-f8" (Re da e8 a f8)
            - "bO-O" oppure "wO-O-O" (arrocco corto e lungo)
            - "bK-e8-x-f8" (Re da e8 mangia in f8)
            - "wP-c7-c8-=wQ" (Pedone va a promozione da c7 a c8)
            - "wP-c7-x-d8-=wQ" (Pedone va a promozione mangiando da c7 a d8)
            - "wP-e5-x-e6-e.p." (Pedone mangia en passant da e5 a e6)
    """
    moves_counter = 0
    def __init__(self, move_string):
        self.move_string = move_string
        t_move.moves_counter += 1

    def get_type(self):
        """
        ritorna una lista di stringa contenente i tipi della mossa
        es:\n
            - ["white","promotion"]
            - ["black","taking","en_passant"]
        """
        type = []

        if self.move_string.startswith("b"):
            type.append("black")
        if self.move_string.startswith("w"):
            type.append("white")
        
        if self.move_string[1:] == "O-O" :
            type.append("castling_short")
        elif self.move_string[1:] == "O-O-O":
            type.append("castling_long")
        else:
            if "x" in self.move_string:
                type.append("taking")
            if "=" in self.move_string:
                type.append("promotion") 
            if "." in self.move_string:
                type.append("en_passant")
        return type
    
    def get_start_end_cord(self):
        cord = {
            "start": None,
            "end": None,
        }
        splitted_move = self.move_string.split("-")
        if "O" in self.move_string:
            pass
        else:
            cord["start"] = t_cord(splitted_move[1])
            if "x" in self.move_string:
                cord["end"] = t_cord(splitted_move[3])
            else:
                cord["end"] = t_cord(splitted_move[2])

        
        return cord
    
    def get_piece(self):
        if "=" in self.move_string:
            return self.move_string[-2:]
        else:
            return self.move_string[:2]
from Connection import Connection

class Game(Connection):
    def __init__(self):
        super().__init__()
        self.init_connection()
    
    #@override
    def do_on_serval(self, ser_val):
        if ser_val == "SHOOT":
            print("SHOOT")
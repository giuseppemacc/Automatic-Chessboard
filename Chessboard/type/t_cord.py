# mi deve indentificare una coordinata 
# sia tramite la forma stringa che tramite la forma a indici
class t_cord():
    """
        string_form = a1,b2... ra1,rb2... la1,lb2...
        index_form = ["grid",[y,x]]... ["left",[y,x]]... ["right",[y,x]]...
    """
    def __init__(self, string_form=None, index_form=None):
        self.string_form = string_form
        self.index_form = index_form
    
    def get_string_form(self):
        if self.string_form == None:
            string_type = self.index_form[0]
            y,x = self.index_form[1]

            self.string_form = ["a","b","c","d","e","f","g","h"][x] + str( [i for i in range(8,0,-1)][y] )

            if string_type == "left":
                self.string_form = "l" + self.string_form
            elif string_type == "right":
                self.string_form = "r" + self.string_form
                
        return self.string_form
    
    def get_index_form(self):
        if self.index_form == None:
            x = ["a","b","c","d","e","f","g","h"].index(self.string_form[-2]) 
            y = 7-(int(self.string_form[-1])-1)
            string_type = ""
            if (self.string_form[0] == "l"):
                string_type = "left"
            elif (self.string_form[0] == "r"):
                string_type = "right"
            else:
                string_type = "grid"

            self.index_form = [string_type,[y,x]]                

        return self.index_form
    
    def __str__(self):
        return f"{self.string_form}"


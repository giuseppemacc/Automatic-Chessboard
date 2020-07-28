class t_cord():
    """
        type of cord:\n
            - "a1" (grid)
            - "wpna1" (panchina white a1)
            - "bpna1" (panchina black a1)
    """
    def __init__(self, cord_string):
        self.cord_string = cord_string

    def get_numeric(self):
        if "pn" in self.cord_string:
            return [["a","b","c","d","e","f","g","h","i"].index(self.cord_string[-2]), 1-(int(self.cord_string[-1])-1)]
        else:
            return [["a","b","c","d","e","f","g","h"].index(self.cord_string[0]), 7-(int(self.cord_string[1])-1)]
    
    def get_string(self):
        return self.cord_string

    def get_spatial(self):
        pass
    
    def get_angles(self):
        pass
    
    def __str__(self):
        return f"{self.cord_string}"

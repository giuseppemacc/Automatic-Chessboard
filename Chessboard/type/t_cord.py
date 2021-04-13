class t_cord():
    """
        type of cord:\n
            - cord_string: "a1" (grid)
            - cord_string: "wpna1" (panchina white a1)
            - cord_string: "bpna1" (panchina black a1)
            - cord_numeric: ["wpn",[y,x]]
    """
    def __init__(self, cord_string=None, cord_numeric=None):
        #TODO: inizializzare cordinata da cord_numeric ["wpn",[y,x]]
        if cord_numeric == None:
            self.cord_string = cord_string
        else:
            if "pn" in cord_numeric[0]:
                self.cord_string = cord_numeric[0]+(["a","b","c","d","e","f","g","h"][cord_numeric[1][1]])+str( [i for i in range(2,0,-1)][cord_numeric[1][0]] )
            else:
                self.cord_string = (["a","b","c","d","e","f","g","h"][cord_numeric[1][1]])+str( [i for i in range(8,0,-1)][cord_numeric[1][0]] ) 


    def get_numeric(self):
        if "pn" in self.cord_string:
            return [self.cord_string[:3], [ 1-(int(self.cord_string[-1])-1), ["a","b","c","d","e","f","g","h"].index(self.cord_string[-2])]]
        else:
            return [self.cord_string[:3], [ 7-(int(self.cord_string[1])-1), ["a","b","c","d","e","f","g","h"].index(self.cord_string[0])]]
    
    def get_string(self):
        return self.cord_string

    def get_spatial(self):
        pass
    
    def get_angles(self):
        pass
    
    def __str__(self):
        return f"{self.cord_string}"

from Chessboard import Chessboard
from type.t_cord import t_cord
from type.t_move import t_move
from PIL import Image
from ImageProcessing import get_dicbool_chessboard

white = [126,110,84]
black = [27,27,27]
offset = {
    "top": 29,
    "bottom": 28,
    "left_int": 17,
    "right_int": 15,
    "left_ext": 3,
    "right_ext":3,
    "color": [10,10]
}

if __name__ == '__main__':
    print("init...")
    
    im_chessboard = Image.open("image/confoglio.jpg").resize((500,375))
    dicbool_chessboard = get_dicbool_chessboard(im_chessboard, offset, [white,black], show_image=True) 
    
    print(dicbool_chessboard["grid"])
    print(dicbool_chessboard["bpn"])
    print(dicbool_chessboard["wpn"])



    print("ending...")
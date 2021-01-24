import numpy as np
from PIL import Image, ImageOps
import os
from AI.PieceRecognition.isPiece import isPiece

offset = {
    "top": 80,
    "bottom": 68,
    "left_int": 35,
    "right_int": 30,
    "left_ext": 20,
    "right_ext":8,
}

def bool_squares(np_squares, dim):
    
    bool_np_chessboard = np.full(dim, None)         
    step = int(np_squares.shape[0]/8)

    y_pixel = 0
    x_pixel = 0

    for y in range(dim[0]):
        y_section_range = [y_pixel, y_pixel+step]
        
        for x in range(dim[1]):
            
            x_section_range = [x_pixel, x_pixel+step]

            section = np.array( [i[x_section_range[0]:x_section_range[1]] for i in np_squares[y_section_range[0]:y_section_range[1]]] )
            
            # bool_np_chessboard[y][x] = True#
            # image = Image.fromarray(np.uint8(section))
            # image.save(f"AI/imageDataSetTest/{string_type}-{y}-{x}.jpg")

            section = np.array(ImageOps.grayscale(Image.fromarray(np.uint8(section)).resize((50,50))))

            if isPiece(section):
               bool_np_chessboard[y][x] = True
            else:
               bool_np_chessboard[y][x] = False 

            x_pixel += step
        x_pixel = 0
        y_pixel += step

    return bool_np_chessboard


def get_dicbool_chessboard(image):
    top = offset["top"]
    bottom = offset["bottom"]
    left_int = offset["left_int"]
    right_int = offset["right_int"]
    left_ext = offset["left_ext"]
    right_ext = offset["right_ext"]
    np_chessboard = np.array(image)
    square = int((image.height - (top + bottom)) / 8) 
    
    """ ritaglia l'immagine """
    # "bpn"
    np_bpn = np.array( [i[left_ext:left_ext+square*2] for i in np_chessboard[top:image.height-bottom]] )
    Image.fromarray(np.uint8(np_bpn)).show()
    # "wpn"
    np_wpn = np.array( [i[-square*2:-right_ext] for i in np_chessboard[top:image.height-bottom]] )
    Image.fromarray(np.uint8(np_wpn)).show()
    # "grid"
    np_grid = np.array( [i[(left_ext+left_int)+square*2:-(right_ext+right_int)-square*2] for i in np_chessboard[top:image.height-bottom]] )
    Image.fromarray(np.uint8(np_grid)).show()


    """ ritorna il dic con la scacchiera boolizzata """
    return {
        "bpn":  np.rot90(bool_squares(np_bpn,(8,2))),
        "wpn":  np.rot90(bool_squares(np_wpn,(8,2))),
        "grid": bool_squares(np_grid,(8,8)),
    }


if __name__ == '__main__':
    
    im_chessboard = Image.open("AI/shoots_test/shoot6.jpg")#.resize((500,375))
    dicbool_chessboard = get_dicbool_chessboard(im_chessboard) 
    print(dicbool_chessboard)
    
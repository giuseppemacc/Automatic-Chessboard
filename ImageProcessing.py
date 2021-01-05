import numpy as np
from PIL import Image, ImageOps
import os
from AI.isPiece import isPiece

white = [68,65,30] #[98,92,58] 
black = [11,13,8] #[3,8,4]
offset = {
    "top": 80,
    "bottom": 68,
    "left_int": 35,
    "right_int": 30,
    "left_ext": 20,
    "right_ext":8,
    "color": [10,10]
}

def _binarize_by2filter(np_image, filter, offset, with_bin_image=False):
    """
    riceve l'np.array di un immagine e ritorna un array di pixel binarizzati in base a due filtri
    """
    filter = np.array(filter)
    # False -> 0 -> nero
    # True -> 255 -> bianco
    np_bin =    np.logical_or(np.logical_and((filter[0] - offset[0]) < np_image, np_image < (filter[0] + offset[0])), \
                np.logical_and((filter[1] - offset[1]) < np_image, np_image < (filter[1] + offset[1])))

    # questo ciclo rende l'rgb dei pixel tutti False nel caso che non fossero tutti True
    for i in range(np_bin.shape[0]):
        for j in range(np_bin.shape[1]):
            if np.array_equal(np_bin[i][j], [True, True, True]):
                pass
            else:
                np_bin[i][j] = [False, False, False]

    if with_bin_image:
        return {"image": Image.fromarray(np.uint8(np_bin * 255)),
                "np": np_bin}
    else:
        return {"np":np_bin}

def _bool_chessboard(bool_np,dim):
    """
    riceve un l'np.array di una sezione della scacchiera (grid o pn) e la dimensione ( (8,8) o (2,8) )
    ritorna un array di quella dimensione con True dove c'è una pedina e False dove non c'è 
    """ 


    bool_np_chessboard = np.full(dim, None)         

    step = int(bool_np.shape[0]/8)
    
    y_pixel = 0
    x_pixel = 0

    for y in range(dim[0]):
        y_section_range = [y_pixel, y_pixel+step]
        
        for x in range(dim[1]):
            
            x_section_range = [x_pixel, x_pixel+step]

            section = np.array( [i[x_section_range[0]:x_section_range[1]] for i in bool_np[y_section_range[0]:y_section_range[1]]] )
            
            count = 0
            for i in section:
                for j in i:
                    if True in j:
                        count+=1

            if count > 20:
                bool_np_chessboard[y][x] = True
            else:
                bool_np_chessboard[y][x] = False 

            x_pixel += step
        x_pixel = 0
        y_pixel += step
            

    return bool_np_chessboard

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
    color = offset["color"]
    np_chessboard = np.array(image)
    square = int((image.height - (top + bottom)) / 8) 
    
    """ritaglia l'immagine"""

    # "bpn"
    np_bpn = np.array( [i[left_ext:left_ext+square*2] for i in np_chessboard[top:image.height-bottom]] )
    Image.fromarray(np.uint8(np_bpn)).show()
    # "wpn"
    np_wpn = np.array( [i[-square*2:-right_ext] for i in np_chessboard[top:image.height-bottom]] )
    Image.fromarray(np.uint8(np_wpn)).show()
    # "grid"
    np_grid = np.array( [i[(left_ext+left_int)+square*2:-(right_ext+right_int)-square*2] for i in np_chessboard[top:image.height-bottom]] )
    Image.fromarray(np.uint8(np_grid)).show()

    return {
        "bpn":  np.rot90(bool_squares(np_bpn,(8,2))),
        "wpn":  np.rot90(bool_squares(np_wpn,(8,2))),
        "grid": bool_squares(np_grid,(8,8)),
    }















    

""" def get_dicbool_chessboard(image, offset, filter, show_image=False):
    top = offset["top"]
    bottom = offset["bottom"]
    left_int = offset["left_int"]
    right_int = offset["right_int"]
    left_ext = offset["left_ext"]
    right_ext = offset["right_ext"]
    color = offset["color"]

    dicbool_chessboard = {
        "bpn": [],
        "wpn": [],
        "grid": []
    }

    np_chessboard = np.array(image)
    square = int((image.height - (top + bottom)) / 8) 

    # dicbool_chessboard["bpn"/"wpn"] la matrice va ruotata di 90 gradi (perchè è di shape (8,2) ma a noi serve (2,8))

    # "bpn"
    np_bpn = np.array( [i[left_ext:left_ext+square*2] for i in np_chessboard[top:image.height-bottom]] )
    dic_bin_bpn = _binarize_by2filter(np_bpn, filter, color, with_bin_image=show_image)
    dicbool_chessboard["bpn"] = np.rot90(_bool_chessboard(dic_bin_bpn["np"],(8,2)))
    
    # "wpn"
    np_wpn = np.array( [i[-square*2:-right_ext] for i in np_chessboard[top:image.height-bottom]] )
    dic_bin_wpn = _binarize_by2filter(np_wpn, filter, color, with_bin_image=show_image)
    dicbool_chessboard["wpn"] = np.rot90(_bool_chessboard(dic_bin_wpn["np"],(8,2)))

    # "grid"
    np_grid = np.array( [i[(left_ext+left_int)+square*2:-(right_ext+right_int)-square*2] for i in np_chessboard[top:image.height-bottom]] )
    dic_bin_grid = _binarize_by2filter(np_grid, filter, color, with_bin_image=show_image)
    dicbool_chessboard["grid"] = _bool_chessboard(dic_bin_grid["np"],(8,8))

    if show_image:
        im_grid = Image.fromarray(np.uint8(np_grid))
        im_grid.show()
        dic_bin_grid["image"].show()
        im_wpn = Image.fromarray(np.uint8(np_wpn))
        im_wpn.show()
        dic_bin_wpn["image"].show()
        im_bpn = Image.fromarray(np.uint8(np_bpn))
        im_bpn.show()
        dic_bin_bpn["image"].show()

    return dicbool_chessboard """

""" Esempio di utilizzo """
if __name__ == '__main__':
    
    """     # create image
        #im_pn = Image.open('image/2_ideal_pn.jpeg').resize((30, 120))
        ##im_pn.show()
        #im_np_pn = np.array(im_pn)

        #im_grid = Image.open('image/2_ideal.jpeg').resize((120, 120))
        ##im_grid.show()
        #im_np_grid = np.array(im_grid)


        # dic_bin è un dizionario contenente l'image binarizzata (bianco e nero) e un array booleano
        # posso anche scegliere di ritornare solo la schacchiera in bool mettendo with_bin_image=False (che lo è già di default) 
        #dic_bin_pn = _binarize_by2filter(im_np_pn, [white,black], [10, 10], with_bin_image=True)
        #dic_bin_pn["image"].show()

        #dic_bin_grid = _binarize_by2filter(im_np_grid, [white,black], [10, 10], with_bin_image=True)
        #dic_bin_grid["image"].show()

        #print(_bool_chessboard(dic_bin_pn["np"],(8,2)))
        #print(_bool_chessboard(dic_bin_grid["np"],(8,8)))

        # with full chessboard """

    im_chessboard = Image.open("AI/shoots_test/shoot6.jpg")#.resize((500,375))
    dicbool_chessboard = get_dicbool_chessboard(im_chessboard) #get_dicbool_chessboard(im_chessboard, offset, [white,black], show_image=True) 
    
    """ print(dicbool_chessboard["grid"])
    print("")
    print(dicbool_chessboard["bpn"])
    print("")
    print(dicbool_chessboard["wpn"]) """
    
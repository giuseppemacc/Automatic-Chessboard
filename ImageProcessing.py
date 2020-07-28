import numpy as np
from PIL import Image
import os

def binarize_by2filter(image, filter, offset, with_bin_image=False):
    """
    riceve un immagine e ritorna un array di pixel binarizzati in base a due filtri
    """
    np_image = np.array(image)
    filter = np.array(filter)
    # False -> 0 -> nero
    # True -> 255 -> bianco
    np_bin =    np.logical_or(np.logical_and((filter[0] - offset[0]) < np_image, np_image < (filter[0] + offset[0])), \
                np.logical_and((filter[1] - offset[1]) < np_image, np_image < (filter[1] + offset[1])))

    for i in range(image.height):
        for j in range(image.width):
            if np.array_equal(np_bin[i][j], [True, True, True]):
                pass
            else:
                np_bin[i][j] = [False, False, False]

    bool_np_checkboard = _bool_checkboard(np_bin)

    if with_bin_image:
        return {"image": Image.fromarray(np.uint8(np_bin * 255)),
                "bool": bool_np_checkboard}
    else:
        return bool_np_checkboard

def _bool_checkboard(bool_np):
    """
    riceve bool_np della scacchiera con ogni singolo pixel binarizzato
    e ritorna bool_np_checkboard come se fosse una scacchiera quindi
    divide bool_np ricevuto come parametro in un 8x8 e se in una casella è presente anche un solo pixel True la casella 
    corrispondente di bool_np_checkboard diventa True
    """
    # TODO permettere di fare la stessa cosa ma con le panchine
    size = int(bool_np.shape[0])
    bool_np_checkboard = np.full((8,8),None)         

    step = int(size/8)
    count_x = 0
    count_y = 0
    for i in range(0, size, step):
        y = [i, i+step]
        for j in range(0, size, step):
            x = [j, j+step]

            cube = np.array( [i[x[0]:x[1]] for i in bool_np[y[0]:y[1]]] )
            # TODO modificare questo if per mettere il controllo di quanti True ci devono essere per far essere tutta True la casella
            if True in cube:
                bool_np_checkboard[count_y][count_x] = True
            else:
                bool_np_checkboard[count_y][count_x] = False

            count_x += 1
        count_x = 0
        count_y += 1

    return bool_np_checkboard

""" Esempio di utilizzo """
if __name__ == '__main__':
    
    # create image
    im = Image.open('image/2_ideal.jpeg').resize((120, 120))
    im.show()

    # white and black filter color
    white = [239,228,176]
    black = [113,71,47] 

    # dic_bin è un dizionario contenente l'image binarizzata (bianco e nero) e un array booleano
    # posso anche scegliere di ritornare solo la schacchiera in bool mettendo with_bin_image=False (che lo è già di default) 
    dic_bin = binarize_by2filter(im, [white,black], [10, 10], with_bin_image=True)
    
    print(dic_bin["bool"])
    dic_bin["image"].show()
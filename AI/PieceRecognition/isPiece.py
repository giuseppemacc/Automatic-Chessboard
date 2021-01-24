import math as mt
import numpy as np
import random as rd
from PIL import Image, ImageOps
from os import listdir
from os.path import isfile, join
import torch
from tqdm import tqdm
from matplotlib import pyplot as plt
from .PieceRecognition import Recognize_PE, calc

recognize_PE = Recognize_PE()
recognize_PE.load_state_dict(torch.load("model3.pt"))
#model.eval()


def isPiece(np_square):
    global recognize_PE
    val = calc(np_square, recognize_PE)
    return (val == 1)
    

if __name__ == "__main__":

    #img = cv2.imread("imageDataSet/Piece/grid3-7-6.jpg", cv2.IMREAD_GRAYSCALE)
    #img = cv2.resize(img, (50, 50))

    img = ImageOps.grayscale(Image.open("imageDataSet/Piece/grid3-7-6.jpg").resize((50,50)))
    
    np_img = np.array(img)
    print(isPiece(np_img))

import numpy as np
import torch
from matplotlib import pyplot as plt
from .PieceRecognition import PieceRecognition, getPattern
from ImageProcessing.PieceRecognition.PieceRecognition import PieceRecognition, getPattern
import cv2

def isPiece(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("",img)
    # cv2.waitKey()

    neural_net = PieceRecognition()
    neural_net.load_state_dict(torch.load("ImageProcessing/PieceRecognition/models/model50.pt"))

    pattern = getPattern(img, neural_net)
    print(pattern)
    return bool(pattern)

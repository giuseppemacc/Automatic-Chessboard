import numpy as np
import torch
from matplotlib import pyplot as plt
from .PieceRecognition import PieceRecognition, getPattern
from ImageProcessing.PieceRecognition.PieceRecognition import PieceRecognition, getPattern
#from PieceRecognition.PieceRecognition import PieceRecognition, getPattern
import cv2

RED_UPPER = [251,69,255]
RED_LOWER = [0,0,81]

BLUE_UPPER = [255,255,49]
BLUE_LOWER = [88,0,0]


def isPiece(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("",img)
    # cv2.waitKey()

    neural_net = PieceRecognition()
    neural_net.load_state_dict(torch.load("ImageProcessing/PieceRecognition/models/model50.pt"))
    #neural_net.load_state_dict(torch.load("PieceRecognition/models/model50.pt"))

    pattern = getPattern(img, neural_net)
    print(pattern)
    return pattern

def getColour(img):
    value = isPiece(img)

    if value == 1:
        def colourMask(lower, upper):
            lower = np.array(lower, dtype = "uint8")
            upper = np.array(upper, dtype = "uint8")
            mask = cv2.inRange(img, lower, upper)
            output = cv2.bitwise_and(img, img, mask = mask)
            return output
        
        def notEmpty_pixel(image):
            count = 0
            for y in image:
                for x in y:
                    x != [0,0,0]
                    if x[0] or x[1] or x[2]:
                        count += 1

            return count


        redMask_img = colourMask(RED_LOWER,RED_UPPER)    
        blueMask_img = colourMask(BLUE_LOWER,BLUE_UPPER) 

        count_blue = notEmpty_pixel(blueMask_img)
        count_red = notEmpty_pixel(redMask_img)

        #print("blue: ", count_blue, "  red:", count_red)

        if count_blue >= count_red:
            return 1
        else:
            return 2

        #cv2.imshow("images", np.hstack([img ,redMask_img, blueMask_img]))
        #cv2.waitKey(0)

    else:
        return value



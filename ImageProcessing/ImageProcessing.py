import cv2
import numpy as np
from ImageProcessing.PieceRecognition.isPiece import isPiece, getColour
from ImageProcessing.PieceRecognition.PieceRecognition import PieceRecognition
import torch

#from PieceRecognition.isPiece import isPiece, getColour

PIECE_RECOGNITION = PieceRecognition()
PIECE_RECOGNITION.load_state_dict(torch.load("ImageProcessing/PieceRecognition/models/model50.pt"))

WIDTH, HEIGHT = 1024,652

LEFT_TOP = [225,168] #[252,169]
RIGH_TOP = [765,163] #[792,157]
LEFT_BOTTOM = [235,507] #[269,504]
RIGH_BOTTOM = [761,502] #[790,495]

PADDING = 15

LEFF_INT_BORDER = 187
LEFF_EXT_BORDER = 157

RIGHT_INT_BORDER = 807
RIGHT_EXT_BORDER = 837

SQUARE_SIZE = (77,77)

def warpChessboard(path):
    img = cv2.imread(path)

    pts1 = np.float32( [LEFT_TOP, RIGH_TOP, LEFT_BOTTOM, RIGH_BOTTOM] )
    pts2 = np.float32( [[0,0], [WIDTH,0], [0,HEIGHT], [WIDTH,HEIGHT]] )
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    warp_img = cv2.warpPerspective(img, matrix, (WIDTH,HEIGHT))

    for x in range(0,4):
        cv2.circle(img, (pts1[x][0], pts1[x][1]), 1, (0,0,255), cv2.FILLED)
    
    # cv2.imshow("Marked Shoot",img)
    # cv2.imwrite("images\marked_shoot.jpg",img)
# 
    # cv2.imshow("Warped Image",warp_img)
    # cv2.imwrite("images\warped_img.jpg",warp_img)
    

    return warp_img
    

def cropImage(img):

    #-----remove border-----
    img_cropped = img[PADDING:HEIGHT-PADDING, PADDING:WIDTH-PADDING]

    img_lpn = img_cropped[  0:HEIGHT , 0:LEFF_EXT_BORDER  ]
    img_rpn = img_cropped[  0:HEIGHT , RIGHT_EXT_BORDER:WIDTH  ]
    img_grid = img_cropped[ 0:HEIGHT , LEFF_INT_BORDER:RIGHT_INT_BORDER ]

    # cv2.imshow("Cropped Image",img_cropped)
    # cv2.imwrite("images\cropped_img.jpg",img_cropped)

    # cv2.imshow("Left Side Image",img_lpn)
    # cv2.imwrite("images\img_lpn.jpg",img_lpn)
    # cv2.imshow("Right Side Image",img_rpn)
    # cv2.imwrite("images\img_rpn.jpg",img_rpn)
    # cv2.imshow("Grid Image",img_grid)
    # cv2.imwrite("images\img_grid.jpg",img_grid)


    #-----crop left side----
    list_img_lpn = []

    height_lpn = img_lpn.shape[0]
    width_lpn = img_lpn.shape[1]

    step_x = int(width_lpn/2)
    step_y = int(height_lpn/8)

    for y in range(8):
        list_img_lpn.append(  [img_lpn[(step_y*y):(step_y*y)+step_y  , 0:step_x ], img_lpn[  (step_y*y):(step_y*y)+step_y  , step_x:width_lpn ]]  )


    #-----crop right side----
    list_img_rpn = []

    height_rpn = img_rpn.shape[0]
    width_rpn = img_rpn.shape[1]

    step_x = int(width_rpn/2)
    step_y = int(height_rpn/8)

    for y in range(8):
        list_img_rpn.append(  [img_rpn[(step_y*y):(step_y*y)+step_y  , 0:step_x ], img_rpn[  (step_y*y):(step_y*y)+step_y  , step_x:width_rpn ]]  )


    #-----crop grid----
    list_img_grid = []

    height_grid = img_grid.shape[0]
    width_grid = img_grid.shape[1]

    step_x = int(width_grid/8)
    step_y = int(height_grid/8)

    for y in range(8):
        list_img_grid.append([ img_grid[ (step_y*y):(step_y*y)+step_y  , (step_x*x):(step_x*x)+step_x ]  for x in range(8)   ])

    #----return dictionary with this images---

    return {
        "right": [ [cv2.resize(img_rpn_x, SQUARE_SIZE) for img_rpn_x in img_rpn_y] for img_rpn_y in list_img_rpn],
        "left":  [ [cv2.resize(img_lpn_x, SQUARE_SIZE) for img_lpn_x in img_lpn_y] for img_lpn_y in list_img_lpn],
        "grid":  [ [cv2.resize(img_grid_x, SQUARE_SIZE) for img_grid_x in img_grid_y] for img_grid_y in list_img_grid],
    }

def binarizes(dic_images):
    return{
        "right": [ [getColour(x_img) for x_img in y_img] for y_img in dic_images["right"]],
        "left":  [ [getColour(x_img) for x_img in y_img] for y_img in dic_images["left" ]],
        "grid":  [ [getColour(x_img) for x_img in y_img] for y_img in dic_images["grid" ]]
    }

def see_Chessboard():
    warped_img = warpChessboard("shoot.jpg")
    crop_img = cropImage(warped_img)
    dic_bin_chessboard = binarizes(crop_img)

    return dic_bin_chessboard



if __name__ == "__main__":
    warped_img = warpChessboard("images\shoot.jpg")
    crop_img = cropImage(warped_img)
    dic_bin_chessboard = binarizes(crop_img)
    cv2.waitKey()
    print(dic_bin_chessboard)

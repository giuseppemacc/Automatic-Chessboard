import os
import numpy as np
from tqdm import tqdm
import torch
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image, ImageOps


BUILD_DATA = True
TRAIN = False
TEST = False

IMG_SIZE = 50
EPOCHS = 300
BATCH_SIZE = 100
LR = 0.001


class DataSet_PE():
    
    PIECE = "imageDataSetTest/Piece"
    EMPTY = "imageDataSetTest/Empty"
    LABELS = {EMPTY: 0, PIECE: 1}
    training_data = []

    piececount = 0
    emptycount = 0

    def make_training_data(self):
        for label in self.LABELS:
            print(label)
            for f in tqdm(os.listdir(label)):
                if "jpg" in f:
                    try:
                        path = os.path.join(label, f)
                        # img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        # img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                        img = ImageOps.grayscale(Image.open(path).resize((IMG_SIZE,IMG_SIZE)))
                        self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])

                        if label == self.EMPTY:
                            self.emptycount += 1
                        elif label == self.PIECE:
                            self.piececount += 1

                    except Exception as e:
                        pass

        np.random.shuffle(self.training_data)
        np.save("test_dataset2.npy", self.training_data)
        print('Piece:',self.piececount)
        print('Empty:',self.emptycount)

class Recognize_PE(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 5) # input is 1 image, 32 output channels, 5x5 kernel / window
        self.conv2 = nn.Conv2d(32, 64, 5) # input is 32, bc the first layer output 32. Then we say the output will be 64 channels, 5x5 kernel / window
        self.conv3 = nn.Conv2d(64, 128, 5)

        x = torch.randn(50,50).view(-1,1,50,50)
        self._to_linear = None
        self.convs(x)

        self.fc1 = nn.Linear(self._to_linear, 512) #flattening.
        self.fc2 = nn.Linear(512, 2) # 512 in, 2 out bc we're doing 2 classes

    def convs(self, x):
        # max pooling over 2x2
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2, 2))

        if self._to_linear is None:
            self._to_linear = x[0].shape[0]*x[0].shape[1]*x[0].shape[2]
        return x

    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, self._to_linear)  # .view is reshape ... this flattens X before 
        x = F.relu(self.fc1(x))
        x = self.fc2(x) # bc this is our output layer. No activation here.
        return F.softmax(x, dim=1)

def train(model, training_dataset):
    X = (torch.Tensor([i[0] for i in training_dataset]).view(-1,50,50))/255
    y = torch.Tensor([i[1] for i in training_dataset])

    # TODO: aggiungere qualcosa per modificare il train set a ogni epoch
    train_X = X 
    train_y = y

    optimizer = optim.Adam(model.parameters(), lr=LR)
    loss_function = nn.MSELoss()

    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_X), BATCH_SIZE)): # from 0, to the len of x, stepping BATCH_SIZE at a time. [:50] ..for now just to dev
            batch_X = train_X[i:i+BATCH_SIZE].view(-1, 1, 50, 50)
            batch_y = train_y[i:i+BATCH_SIZE]

            model.zero_grad()

            outputs = model(batch_X)
            loss = loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()    # Does the update

        print(f"Epoch: {epoch}. Loss: {loss}")
    
    torch.save(model.state_dict(), "model2.pt")


def calc(np_img, model):
    predicted = 0
    with torch.no_grad():
        X_img = torch.Tensor(np_img).view(-1,50,50)
        X_img = X_img/255.0

        net_out = model(X_img.view(-1, 1, 50, 50))[0]  
        predicted = int(torch.argmax(net_out))
    return predicted

def test(model, test_dataset):

    X = [i[0] for i in test_dataset]
    y = [i[1] for i in test_dataset]

    correct = 0
    total = 0

    for i in tqdm(range(len(X))):
        predicted = calc(X[i], model)
        real = torch.argmax(torch.Tensor(y[i]))
        print(f"predicted:{predicted}    real:{real}")
        if predicted == real:
            correct += 1
        else:
            plt.imshow(X[i], cmap="gray")
            plt.show()
        total += 1
    print(f"correct:{correct}  total:{total}  accuracy:{round(correct/total, 3)}")

if __name__ == "__main__":

    if BUILD_DATA:
        dataset_PE = DataSet_PE()
        dataset_PE.make_training_data()

    if TRAIN or TEST:
        recognize_PE = Recognize_PE()
        recognize_PE.load_state_dict(torch.load("model1000.pt"))

        training_dataset = np.load("test_dataset.npy", allow_pickle=True)
        np.random.shuffle(training_dataset)
        

        if TRAIN:
            train(recognize_PE, training_dataset)
        if TEST:
            test(recognize_PE, training_dataset)
    

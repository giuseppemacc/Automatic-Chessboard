import os
import numpy as np
from tqdm import tqdm
import torch
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import cv2


BUILD_DATA = False
TRAIN = False
TEST = False

IMG_SIZE = 77
EPOCHS = 50
BATCH_SIZE = 100
LR = 0.001


class DataSet():
    
    def __init__(self, path):
        self.path = path
        
        self.PATTERN_0 = f"DataSet/{path}/PATTERN_0"
        self.PATTERN_1 = f"DataSet/{path}/PATTERN_1"

        self.LABELS = {self.PATTERN_0: 0, self.PATTERN_1: 1}
        self.training_data = []

        self.pattern0_count = 0
        self.pattern1_count = 0

    def make_data(self):
        for label in self.LABELS:
            print(label)
            for f in tqdm(os.listdir(label)):
                if "jpg" in f:
                    try:
                        #path = os.path.join(label, f)
                        #img = ImageOps.grayscale(Image.open(path).resize((IMG_SIZE,IMG_SIZE)))

                        path = os.path.join(label, f)
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))

                        self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])

                        if label == self.PATTERN_0:
                            self.pattern0_count += 1
                        elif label == self.PATTERN_1:
                            self.pattern1_count += 1

                    except Exception as e:
                        pass

        np.random.shuffle(self.training_data)
        np.save(f"DataSet/{self.path}/dataset.npy", self.training_data)
        print('PATTERN_0:',self.pattern0_count)
        print('PATTERN_1:',self.pattern1_count)

class PieceRecognition(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 5) 
        self.conv2 = nn.Conv2d(32, 64, 5)
        self.conv3 = nn.Conv2d(64, 128, 5)

        x = torch.randn(IMG_SIZE,IMG_SIZE).view(-1,1,IMG_SIZE,IMG_SIZE)
        self._to_linear = None
        self.convs(x)

        self.fc1 = nn.Linear(self._to_linear, 512)
        self.fc2 = nn.Linear(512, 2)

    def convs(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv3(x)), (2, 2))

        if self._to_linear is None:
            self._to_linear = x[0].shape[0]*x[0].shape[1]*x[0].shape[2]
        return x

    def forward(self, x):
        x = self.convs(x)
        x = x.view(-1, self._to_linear) 
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.softmax(x, dim=1)

def train(model, training_dataset):
    X = (torch.Tensor([i[0] for i in training_dataset]).view(-1,IMG_SIZE,IMG_SIZE))/255
    y = torch.Tensor([i[1] for i in training_dataset])

    # TODO: add something to change the train set at each epoch
    train_X = X 
    train_y = y

    optimizer = optim.Adam(model.parameters(), lr=LR)
    loss_function = nn.MSELoss()

    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_X), BATCH_SIZE)):
            batch_X = train_X[i:i+BATCH_SIZE].view(-1, 1, IMG_SIZE, IMG_SIZE)
            batch_y = train_y[i:i+BATCH_SIZE]

            model.zero_grad()

            outputs = model(batch_X)
            loss = loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()   

        print(f"Epoch: {epoch}. Loss: {loss}")
    
    torch.save(model.state_dict(), f"models/model{EPOCHS}.pt", _use_new_zipfile_serialization=False)


def getPattern(np_img, model):
    predicted = 0
    with torch.no_grad():
        X_img = torch.Tensor(np_img).view(-1,IMG_SIZE,IMG_SIZE)
        X_img = X_img/255.0

        net_out = model(X_img.view(-1, 1, IMG_SIZE, IMG_SIZE))[0]  
        predicted = int(torch.argmax(net_out))
    return predicted

def test(model, test_dataset):

    X = [i[0] for i in test_dataset]
    y = [i[1] for i in test_dataset]

    correct = 0
    total = 0

    for i in tqdm(range(len(X))):
        predicted = getPattern(X[i], model)
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
        train_dataset = DataSet("TRAIN")
        train_dataset.make_data()

        test_dataset = DataSet("TEST")
        test_dataset.make_data()

    if TRAIN or TEST:
        image_recognition = PieceRecognition()

        if TRAIN:
            
            train_dataset = np.load("DataSet/TRAIN/dataset.npy", allow_pickle=True)
            np.random.shuffle(train_dataset)

            train(image_recognition, train_dataset)

        if TEST:

            test_dataset = np.load("DataSet/TEST/dataset.npy", allow_pickle=True)
            np.random.shuffle(test_dataset)

            image_recognition.load_state_dict(torch.load("models/model300.pt"))
            test(image_recognition, test_dataset)
    

import os
import cv2
import numpy as np
from tqdm import tqdm
import torch
import torchvision
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


REBUILD_DATA = False

class DataSet_PE():
    IMG_SIZE = 50
    PIECE = "imageDataSet/Piece"
    EMPTY = "imageDataSet/Empty"
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
                        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        img = cv2.resize(img, (self.IMG_SIZE, self.IMG_SIZE))
                        self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])

                        if label == self.EMPTY:
                            self.emptycount += 1
                        elif label == self.PIECE:
                            self.piececount += 1

                    except Exception as e:
                        pass

        np.random.shuffle(self.training_data)
        np.save("training_data.npy", self.training_data)
        print('Piece:',dataset_PE.piececount)
        print('Empty:',dataset_PE.emptycount)

class Net(nn.Module):
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


net = Net()

if REBUILD_DATA:
    dataset_PE = DataSet_PE()
    dataset_PE.make_training_data()

training_data = np.load("training_data.npy", allow_pickle=True)

optimizer = optim.Adam(net.parameters(), lr=0.001)
loss_function = nn.MSELoss()

np.random.shuffle(training_data)

X = torch.Tensor([i[0] for i in training_data]).view(-1,50,50)
X = X/255.0
y = torch.Tensor([i[1] for i in training_data])

VAL_PCT = 0.1  # lets reserve 10% of our data for validation
val_size = int(len(X)*VAL_PCT)

train_X = X[:-val_size]
train_y = y[:-val_size]

test_X = X[-val_size:]
test_y = y[-val_size:]

BATCH_SIZE = 100
EPOCHS = 1000


def train(net):
    for epoch in range(EPOCHS):
        for i in tqdm(range(0, len(train_X), BATCH_SIZE)): # from 0, to the len of x, stepping BATCH_SIZE at a time. [:50] ..for now just to dev
            #print(f"{i}:{i+BATCH_SIZE}")
            batch_X = train_X[i:i+BATCH_SIZE].view(-1, 1, 50, 50)
            batch_y = train_y[i:i+BATCH_SIZE]

            net.zero_grad()

            outputs = net(batch_X)
            loss = loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()    # Does the update

        print(f"Epoch: {epoch}. Loss: {loss}")


def calc(np_img, model):
    predicted = 0
    with torch.no_grad():
        X_img = torch.Tensor(np_img).view(-1,50,50)
        X_img = X_img/255.0

        net_out = model(X_img.view(-1, 1, 50, 50))[0]  
        predicted = int(torch.argmax(net_out))
    return predicted


def test(NET):
    correct = 0
    total = 0
    with torch.no_grad():
        for i in tqdm(range(len(test_X))):
            real_class = int(torch.argmax(test_y[i]))

            #net_out = NET(test_X[i].view(-1, 1, 50, 50))[0]  

            predicted_class = calc(test_X[i], NET)


            if predicted_class == real_class:
                correct += 1
            total += 1

            print(f" calculated:{int(predicted_class)}   real:{int(real_class)}")
            print(f"correct:{correct}   total:{total}")

            """ """ plt.imshow(test_X[i].view(50,50), cmap="gray")
            plt.show()  """
 """
    print("Accuracy: ", round(correct/total, 3))


test(model):
    training_data = np.load("training_data.npy", allow_pickle=True)

    X = [i[0] for i in training_data]
    y = [i[1] for i in training_data]


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
    print("Accuracy: ", round(correct/total, 3))


if __name__ == "__main__":

    train(net)
    torch.save(net.state_dict(), "model.pt")

    # model = Net()
    # model.load_state_dict(torch.load("model.pt"))
    # model.eval()

    # test(model)





    
    

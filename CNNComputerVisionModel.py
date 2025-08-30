#!/usr/bin/env python
# coding: utf-8

# In[26]:


import torch
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
from tqdm.auto import tqdm


# In[10]:


trainData = datasets.FashionMNIST(train=True, root='data', download=True, transform=ToTensor(), target_transform=None)
# Dont transform the labels of the data
testDataLoader = datasets.FashionMNIST(train=False, root='data', download=True, transform=ToTensor())


# In[11]:


image, label = trainData[0]


# In[12]:


classNames = trainData.classes
print(classNames)


# In[17]:


trainDataLoader = DataLoader(trainData, batch_size=32, shuffle=True)
testData = DataLoader(testData, batch_size=32, shuffle=False)
print(len(trainDataLoader), len(testDataLoader))


# In[18]:


device = 'cuda' if torch.cuda.is_available() else "cpu"


# In[42]:


class FashinMNIST2(nn.Module):
    def __init__(self, inputShape:int, hiddenUnits:int, outputShape:int):
        super().__init__()
        self.Block1 = nn.Sequential(
            nn.Conv2d(in_channels=inputShape, out_channels=outputShape, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=hiddenUnits, out_channels=hiddenUnits, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.Block2 = nn.Sequential(
            nn.Conv2d(hiddenUnits, hiddenUnits, stride=1, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(hiddenUnits, hiddenUnits, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.Classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=hiddenUnits * 7 * 7, out_features=outputShape)
        )
    def forward(self, x):
        x = self.Block1(x)
        x = self.Block2(x)
        x = self.Classifier(x)
        return x


# In[43]:


torch.manual_seed(69)
model2 = FashinMNIST2(inputShape=1, hiddenUnits=10, outputShape=len(classNames)).to(device)


# In[44]:


print(model2)


# In[45]:


lossFunction = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(params=model2.parameters(), lr = 0.01)


# In[46]:


def accuracyFunction(yTrue, yPred):
    correct = torch.eq(yTrue, yPred).sum().item()
    acc = (correct/len(yPred)) * 100
    return acc


# In[47]:


def printTime(startTime:float, endTime:float, device:torch.device=None):
    time = endTime - startTime
    print(f"Total time on {device}: {time:.3f} seconds")
    return time


# In[65]:


def trainStep(dataLoader:torch.utils.data.DataLoader, model:nn.Module,
               optimizer:torch.optim.Optimizer,accuracyFunction, device:torch.device, lossFunction:torch.nn.Module):
    for batch, (X,y) in enumerate(trainDataLoader):
        trainLoss, trainAcc = 0, 0
        X, y = X.to(device), y.to(device)
        yPred = model(X)
        loss = lossFunction(yPred, y)
        trainLoss += loss
        trainAcc += accuracyFunction(yPred=yPred.argmax(dim=1), yTrue=y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    trainLoss /= len(dataLoader)
    trainLoss /= len(dataLoader)
    print(f"Train Loss:{trainLoss:5f} || Train Accuracy: {trainAcc:.2f}\n")



# In[64]:


def testStep(dataLoader:torch.utils.data.DataLoader, model:nn.Module, device:torch.device, lossFunction:torch.nn.Module, accuracyFunction):
    testLoss, testAcc = 0, 0
    model.to(device)
    model.eval()
    with torch.inference_mode():
        for X, y in dataLoader:
            testPred = model(X)
            loss = lossFunction(testPred, y)
            testLoss += loss
            testAcc += accuracyFunction(yTrue=y, yPred=testPred.argmax(dim=1))
        testLoss /= len(dataLoader)
        testAcc /= len(dataLoader)
        print(f"Test Loss :{testLoss:.5f} || Test Accuracy: {testAcc:.2f}\n")


# In[ ]:


torch.manual_seed(69)

from timeit import default_timer as timer
trainStartTime = timer()

epochs = 3
for epoch in tqdm(range(epochs)):
    print(f"Epoch {epoch}\n--------------------")

    trainStep(dataLoader=trainDataLoader, model=model2, lossFunction=lossFunction, optimizer=optimizer, accuracyFunction=accuracyFunction, device=device)
    testStep(dataLoader=testDataLoader, model=model2, lossFunction=lossFunction, accuracyFunction=accuracyFunction, device=device)

trainEndTime = timer()
totalTrainTime = printTime(startTime=trainStartTime, endTime=trainEndTime, device=device)


# In[ ]:





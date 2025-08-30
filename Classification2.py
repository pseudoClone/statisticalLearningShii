import matplotlib.pyplot as plt
import torch
from torch import float32, nn
from pathlib import Path

weight = 0.7
bias = 0.3

X = torch.arange(0, 1, 0.02).unsqueeze(dim=1)

y = weight * X + bias

train_split = int(0.8 * len(X))
X_train, y_train = X[:train_split], y[:train_split]
X_test, y_test = X[train_split:], y[train_split:]

class LinRegModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()

        self.weights = nn.Parameter(data=torch.randn(1, dtype=torch.float32, requires_grad=True))
        self.bias = nn.Parameter(data=torch.randn(1, dtype=torch.float32), requires_grad=True)

    def forward(self, x:torch.Tensor) -> torch.Tensor:
        return(self.weights * x + self.bias)

torch.manual_seed(69)


model = LinRegModel()
modelParams = model.parameters()
print(list(modelParams))

with torch.inference_mode():
    yPreds = model(X_test)


lossFunction = nn.L1Loss()
optimizer = torch.optim.SGD(params=model.parameters(), lr=0.01) # print(modelParams, lr = 0.01) generates error as empty list idk

epochs = 1000

trainLossVals = []
testLossVals = []
epochCount = []

for epoch in range(epochs):

    model.train()

    yPred = model(X_train)

    loss = lossFunction(yPred, y_train)

    optimizer.zero_grad() # Can be set to None too
    loss.backward()
    optimizer.step()

    ## For testing

    model.eval()
    with torch.inference_mode():
        testPred = model(X_test)
        testLoss = lossFunction(testPred, y_test.type(dtype=float32))

        if(epoch % 10 == 0):
            epochCount.append(epoch)
            trainLossVals.append(loss.detach().numpy())
            testLossVals.append(testLoss.detach().numpy())
            print(f"Epoch: {epoch} | MAE Train Loss: {loss} | MAE Test Loss: {testLoss} ")


plt.plot(epochCount, trainLossVals, label="Train Loss")
plt.plot(epochCount, testLossVals, label = "Test Loss")
plt.title("Training and Test Loss")
plt.legend()
plt.ylabel("Loss")
plt.xlabel("Epoch")
plt.show()

print(f"The model learned the following parameters: {model.state_dict()}")
print(f"The weight: {weight}, bias: {bias}")


MODEL_PATH = Path("models")
MODEL_PATH.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "someShitModel.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME
torch.save(obj=model.state_dict(), f=MODEL_SAVE_PATH)
print("MODEL PARAMETERS SAVED")

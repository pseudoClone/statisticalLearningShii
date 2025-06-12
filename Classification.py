import torch
from torch import float32, nn

weights = 0.7
bias = 0.3

start = 0
end = 1
step = 0.02

X = torch.arange(start, end, step).unsqueeze(dim = 1) # Add extra dim to X along the range no the samples
y = weights * X + bias

# print(X[:10], y[:10])

train_split = int(0.8 * len(X))
X_train, y_train = X[:train_split], y[:train_split]
X_test, y_test = X[train_split:], y[train_split:]

class LinearRegressionModel(nn.Module): # As mentioned in the docs, base class for all neural networks
    def __init__(self) -> None:
        super().__init__()
        self.weights = nn.Parameter(torch.randn(1, dtype=float32, requires_grad=True))
        self.bias = nn.Parameter(torch.randn(1, dtype=float32, requires_grad=True))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return (self.weights * x + self.bias)

torch.manual_seed(69)
modelx = LinearRegressionModel()

lossFunction = nn.L1Loss() # MSE
optimizer = torch.optim.SGD(params=modelx.parameters()) # Gets the parameters from the autograd engine
epochs = 100

trainLossVals = []
testLossVals = []
epochCount = []

for epoch in range(epochs):
    modelx.train()

    yPred = modelx.forward(X_train)
    loss = lossFunction(yPred, y_train)
    optimizer.zero_grad() # Can also be set to None but just reset to 0 for now
    loss.backward()

    optimizer.step()

    modelx.eval()

    with torch.inference_mode(): # only use when operations have no interaction with autograd engine
        testPred = modelx.forward(X_test)

        testLoss = lossFunction(testPred, y_test.type(dtype=float32))
        epochCount.append(epoch)
        trainLossVals.append(loss.detach().numpy())
        testLossVals.append(testLoss.detach().numpy())
        print(f"Epoch:{epoch} | MAE Train Loss: {loss} | MAE Test Loss: {testLoss}")

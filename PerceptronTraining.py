import numpy as np
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt

X, y = make_classification(n_samples=1000, n_classes=2, random_state=69, n_features=8, n_informative=2, n_redundant=0)

plt.scatter(X[:,0], X[:,1], c = y, cmap='bwr')
plt.title('Synthetic Dataset')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

class Perceptron:
    def __init__(self, epochs = 1000, lr = 0.01):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def predict(self,X):
        linearOutput = np.dot(X, self.weights) + self.bias
        return np.where(linearOutput >= 0, 1, 0) # Condition vs Broadcast. Dont forget you muppet

    def train(self, X, y):
        yPred = self.predict(X)

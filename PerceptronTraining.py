import numpy as np
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_classes=2, random_state=69,
                           n_features=4, n_informative=2, n_redundant=0)


class Perceptron:
    def __init__(self, epochs=1000, lr=0.01):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def predict(self, X):
        linearOutput = np.dot(X, self.weights) + self.bias
        return np.where(linearOutput >= 0, 1, 0)
        # Classification so need to convert labels to 1 or 0
        # Condition vs Broadcast. Dont forget you muppet

    def train(self, X, y):
        yPred = self.predict(X)
        error = y - yPred
        self.weights += self.lr * error * X
        self.bias += self.lr * error

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)  # Can be anything hai
        self.bias = 0

        for _ in range(self.epochs):
            for x_i, y_i in zip(X, y):
                self.train(x_i, y_i)


model = Perceptron(lr=0.01, epochs=1000)

model.fit(X, y)
yPred = model.predict(X)

accuracy = np.mean(yPred == y)
print(f"Accuracy:{accuracy}")

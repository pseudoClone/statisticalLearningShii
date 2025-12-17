import numpy as np

# Define the OR gate truth table
T = 1.0
F = 0.0

def getORDate():
    X = np.array([
            [F, F],
            [F, T],
            [T, F],
            [T, T]
    ])
    y = np.array([[F], [T], [T], [T]])
    return X, y

X, y = getORDate()

class Perceptron:
    def __init__(self, learningRate = 0.01, epoch = 1000) -> None:
        self.lr = learningRate
        self.epoch = epoch
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        # Initialize weights and bias
        self.weights = np.zeros(X.shape[1])
        self.bias = 0

        # Training loop
        for _ in range(self.epoch):
            for i in range(X.shape[0]):
                # Calculate the dot product and apply activation function
                yPred = self.activationFunc(np.dot(self.weights, X[i]) + self.bias)
                # Compute error
                meanSqErr = y[i] - yPred

                # Update weights and bias
                self.weights = self.weights + self.lr * meanSqErr * X[i]
                self.bias = self.bias + self.lr * meanSqErr

    def activationFunc(self, activation):
        # Step activation function
        if activation > 0:
            return 1
        else:
            return 0

    def predict(self, X):
        # Predict for new data
        predictions = []
        for i in range(X.shape[0]):
            result = self.activationFunc(np.dot(self.weights, X[i]) + self.bias)
            predictions.append(result)
        return np.array(predictions).reshape(-1, 1)


# Initialize and train perceptron
clf = Perceptron()
clf.fit(X, y)

# Test data
X_test = np.array([[F, F], [T, F], [F, T], [T, T]])
y_test = np.array([[F], [T], [T], [T]])

# Make predictions
y_pred = clf.predict(X_test)

print("Predictions:\n", y_pred)

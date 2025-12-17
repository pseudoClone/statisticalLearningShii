import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

n_samples = 1000
n_features = 20

data = np.random.randn(n_samples,n_features)

scaler = MinMaxScaler()
data = scaler.fit_transform(data)

data_tensor = torch.tensor(data, dtype=torch.float32)


class AutoEncoder(nn.Module):
        def __init__(self, input_dim, encoding_dim):
                super(AutoEncoder, self).__init__() # Call the base class constructor i.e nn.Module
                self.encoder = nn.Sequential(
                        nn.Linear(input_dim, 14),
                        nn.LeakyReLU(0.2),
                        nn.BatchNorm1d(14),  # Batch Normalization
                        nn.Linear(14, 8),
                        nn.LeakyReLU(0.2),
                        nn.BatchNorm1d(8),  # Batch Normalization
                        nn.Linear(8, encoding_dim),
                        nn.LeakyReLU(0.2)
                )
                self.decoder = nn.Sequential(
                        nn.Linear(encoding_dim, 14),
                        nn.ReLU(),
                        nn.Linear(14, input_dim),
                        nn.Sigmoid()
                )
        def forward(self, x):
                encoded = self.encoder(x)
                decoded = self.decoder(encoded)
                return decoded

model = AutoEncoder(input_dim=n_features, encoding_dim=7)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001, weight_decay=0.00001)

num_epochs = 200
batch_size = 32
num_batches = len(data)//batch_size

for epoch in range(num_epochs):
        permutation = torch.randperm(data_tensor.size(0))
        for i in range(0, len(data), batch_size):
                indices = permutation[i: i+batch_size]
                batch_data = data_tensor[indices]
                # batch_data = torch.tensor(data[i:i+batch_size], dtype=torch.float32)
                optimizer.zero_grad

                reconstructed = model(batch_data)

                loss = criterion(reconstructed, batch_data)

                loss.backward()
                optimizer.step()

        print(f"Epoch -  [{epoch + 1}] / {num_epochs} :: Loss - {loss.item():.4f}")

with torch.no_grad(): # Eval
        reconstructed_data = model(data_tensor)
original_data = data_tensor.numpy()
reconstructed_data = reconstructed_data.numpy()

plt.figure(figsize=(10,10))

plt.subplot(1,2,1)

plt.scatter(original_data[:, 0], original_data[:, 1], color='blue', label='Original Data') # The first two features in original data, say the samples
plt.title('Original Data')

plt.subplot(1,2,2)
plt.scatter(reconstructed_data[:,0], reconstructed_data[:, 1], color="red", label="Reconstructed Data")
plt.title('Reconstructed Data')
plt.show()

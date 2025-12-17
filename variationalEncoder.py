import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torch.nn.functional as F
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

class Encoder(nn.Module):
    def __init__(self, input_dims, latent_dims):
        super().__init__()
        self.fcl1 = nn.Linear(input_dims, 400)
        self.fcl2 = nn.Linear(400, 200)
        self.fcl3_mu = nn.Linear(200, latent_dims)
        self.fcl3_logvar = nn.Linear(200, latent_dims)

    def forward(self, x):
        h = torch.relu(self.fcl1(x))
        h = torch.relu(self.fcl2(h))
        mu = self.fcl3_mu(h)
        logvar = self.fcl3_logvar(h)
        return mu, logvar

class Decoder(nn.Module):
    def __init__(self, latent_dims, output_dims):
        super(Decoder, self).__init__()
        self.fcl1 = nn.Linear(latent_dims, 200)
        self.fcl2 = nn.Linear(200, 400)
        self.fcl3 = nn.Linear(400, output_dims)

    def forward(self, z):
        h = torch.relu(self.fcl1(z))
        h = torch.relu(self.fcl2(h))
        return torch.sigmoid(self.fcl3(h))

class VAE(nn.Module):
    def __init__(self, input_dims, latent_dims):
        super(VAE, self).__init__()
        self.encoder = Encoder(input_dims, latent_dims)
        self.decoder = Decoder(latent_dims, input_dims)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        epsilon = torch.randn_like(std).to(mu.device)  # IDK, somehow epsilon is not in the same device as the model
        z = mu + epsilon * std
        return z

    def forward(self, x):
        mu, logvar = self.encoder(x)
        z = self.reparameterize(mu, logvar)
        reconstructed_x = self.decoder(z)
        return reconstructed_x, mu, logvar

def vae_loss(reconstructed_x, x , mu, logvar):
    BCE = F.binary_cross_entropy(reconstructed_x, x, reduction='sum')


    KL_divergence = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return BCE + KL_divergence

# Training Loop
def train(model, train_loader, optimizer, epochs=10, device=device):
    model.to(device)
    model.train()
    for epoch in range(epochs):
        train_loss = 0
        for batch_idx, (data, _) in enumerate(train_loader):
            data = data.to(device)
            data = data.view(-1, 784)
            optimizer.zero_grad()
            reconstructed_batch, mu, logvar = model(data)
            loss = vae_loss(reconstructed_x=reconstructed_batch, x=data, mu=mu, logvar=logvar)
            loss.backward()
            train_loss += loss.item()
            optimizer.step()
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {train_loss / len(train_loader.dataset)}")

transform = transforms.Compose([transforms.ToTensor(), transforms.Lambda(lambda x: x.view(-1))])
train_dataset = datasets.MNIST(root=".", train=True, download=True, transform=transform)
train_loader = DataLoader(dataset=train_dataset, batch_size=128, shuffle=True)

input_dims = 784  # 28x28
latent_dims = 20
model = VAE(input_dims, latent_dims).to(device=device)
optimizer = optim.Adam(model.parameters(), lr=1e-4)

train(model=model, train_loader=train_loader, optimizer=optimizer, epochs=10)

def generate_samples(model, num_samples=10, device="cuda"):
    model.eval()
    with torch.no_grad():
        z = torch.randn(num_samples, latent_dims).to(device)
        generated_images = model.decoder(z)
        return generated_images.view(-1, 28, 28)

samples = generate_samples(model=model, num_samples=10, device=device)

fig, axes = plt.subplots(1, 10, figsize=(15, 3))
for i, ax in enumerate(axes):
    ax.imshow(samples[i].cpu().numpy(), cmap='gray')
    ax.axis('off')
plt.show()

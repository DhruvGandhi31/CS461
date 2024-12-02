import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # Normalize for MNIST
])

train_set = torchvision.datasets.MNIST(
    "./data/", train=True, download=True, transform=transform)
test_set = torchvision.datasets.MNIST(
    "./data/", train=False, download=True, transform=transform)

batch_size = 64
train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_set, batch_size=batch_size)

# Define Model


class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(MLP, self).__init__()
        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.model(x)


input_size = 28 * 28
hidden_size = 512
output_size = 10

model = MLP(input_size, hidden_size, output_size).to(device)
print(model)

# Loss and Optimizer
loss_function = nn.CrossEntropyLoss()
optimizer = Adam(model.parameters(), lr=0.001)

# Training and Validation Functions


def train(model, train_loader, loss_function, optimizer, epoch):
    model.train()
    total_loss = 0
    correct = 0
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        output = model(x)
        loss = loss_function(output, y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        pred = output.argmax(dim=1)
        correct += pred.eq(y).sum().item()

    print(f"Epoch {epoch}: Train Loss: {total_loss:.4f}, Train Accuracy: {100 * correct / len(train_loader.dataset):.2f}%")


def validate(model, test_loader, loss_function):
    model.eval()
    total_loss = 0
    correct = 0
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            output = model(x)
            loss = loss_function(output, y)
            total_loss += loss.item()
            pred = output.argmax(dim=1)
            correct += pred.eq(y).sum().item()

    print(
        f"Validation Loss: {total_loss:.4f}, Validation Accuracy: {100 * correct / len(test_loader.dataset):.2f}%")


# Training Loop
epochs = 5
for epoch in range(1, epochs + 1):
    train(model, train_loader, loss_function, optimizer, epoch)
    validate(model, test_loader, loss_function)

# Show Predictions


def show_predictions(model, test_loader):
    model.eval()
    x, y = next(iter(test_loader))
    x, y = x.to(device), y.to(device)
    with torch.no_grad():
        output = model(x)
        pred = output.argmax(dim=1)

    # Visualize the first 10 images and predictions
    plt.figure(figsize=(12, 6))
    for i in range(10):
        plt.subplot(2, 5, i + 1)
        plt.imshow(x[i].cpu().squeeze(), cmap='gray')
        plt.title(f"True: {y[i].item()}, Pred: {pred[i].item()}")
        plt.axis('off')
    plt.tight_layout()
    plt.show()


show_predictions(model, test_loader)

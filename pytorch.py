
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


# 1. Get Data Loader
def get_data_loader(training=True):
    custom_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    dataset = datasets.FashionMNIST(root='./data', train = training, transform=custom_transform)
    #dataset = datasets.FashionMNIST(root='./data', train=False, transform=custom_transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=64)
    return dataloader

# 2. Build Model

def build_model():
    model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28*28, 128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 10)
    )
    return model

def train_model(model, train_loader, criterion, T):
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum = 0.9)
    for i in range(T):
        running_loss = 0.0
        correct = 0
        total = 0
        # get the inputs ; data is a list of [inputs, labels]
        for inputs, labels in train_loader:
            #zero the paremeter gradients
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            # Calculate accuracy
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        accuracy = 100 * correct / total
        print(f"Train Epoch: {i}, Accuracy: {correct}/{total} ({accuracy:.2f}%), Loss: {running_loss/len(train_loader):.3f}")
    # model - the model produced by the previous function
    # train_loader - the train DataLoader produced in first function
    # criterion - cross-entropy
    # T - number of epochs for training

#train_loader = get_data_loader()
#print(train_loader.dataset)
model = build_model()
model.train
train_loader = get_data_loader()
test_loader = get_data_loader(False)
criterion = nn.CrossEntropyLoss()
train_model(model, train_loader, criterion, T=5)


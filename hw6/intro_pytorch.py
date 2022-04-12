import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    if(training):
        train_set=datasets.FashionMNIST("./data",train=True,
            download=True,transform=custom_transform) 
        loader = torch.utils.data.DataLoader(train_set, batch_size = 64)
    if(training == False):
        test_set=datasets.FashionMNIST("./data", train=False,
            transform=custom_transform)
        loader = torch.utils.data.DataLoader(test_set, batch_size = 64, shuffle = False)
    return loader


def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
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
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    size = len(train_loader.dataset)
    model.train()
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    for t in range(T):
        correct, incorrect = 0, 0
        for batch, (X, y) in enumerate(train_loader):
            #X, y = X.to(device), y.to(device)
            # Compute prediction error
            pred = model(X)
            loss = criterion(pred, y)
    
            # Backpropagation
            opt.zero_grad()
            loss.backward()
            opt.step()
            
            #test_loss += loss_fn(pred, y).item()
            #correct += (pred.argmax(1) == y).type(torch.float).sum().item()
            correct += int((pred.argmax(1) == y).type(torch.float).sum().item())
            incorrect += loss.item()
        incorrect /= len(train_loader)
        print(f"Train Epoch: {t}  Accuracy: {correct}/{size}({(100*correct/size):>0.2f}%)"
              + f"  Loss: {incorrect:>0.3f}")




def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    size = len(test_loader.dataset)
    num_batches = len(test_loader)
    model.eval()
    loss, correct = 0, 0
    with torch.no_grad():
        for X, y in test_loader:
            pred = model(X)
            loss += criterion(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    loss /= num_batches
    correct /= size
    if(show_loss):
        print(f"Average loss: {loss:>0.4f}\nAccuracy: {(100*correct):>0.2f}%")
    else:
        print(f"Accuracy: {(100*correct):>0.2f}%")


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt',
                   'Sneaker','Bag','Ankle Boot']
    model.eval()
    x = test_images[index, 0, :, :].float()
    with torch.no_grad():
        pred = model(x.reshape([1, 1, 28, 28]))
        #print(pred)
        prob = F.softmax(pred, dim=1)
        #print(prob)
        res =  torch.argsort(prob, dim=1, descending = True)
        #print(res[0])
        for i in range(3):
            predicted = class_names[res[0][i]]
            print(f"{predicted}: {100*prob[0][res[0][i]]:>0.2f}%")

def main():
    train_loader = get_data_loader()
    #print(type(train_loader))
    #print(train_loader.dataset)
    test_loader = get_data_loader(False)
    #print(type(test_loader))
    #print(test_loader.dataset)
    model = build_model()
    #print(model)
    criterion = nn.CrossEntropyLoss()
    train_model(model, train_loader, criterion, 5)
    evaluate_model(model, test_loader, criterion, show_loss = False)
    evaluate_model(model, test_loader, criterion, show_loss = True)
    predict_label(model, test_loader.dataset.data.reshape([10000, 1, 28, 28]), 0)

if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    main()

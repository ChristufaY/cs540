from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    # Your implementation goes here!
    x = np.load(filename)
    return x - np.mean(x, axis = 0)

def get_covariance(dataset):
    # Your implementation goes here!
    x = dataset - np.mean(dataset, axis = 0)
    return np.dot(np.transpose(x), x)/(len(x) - 1)

def get_eig(S, m):
    # Your implementation goes here!
    v1, v2 = eigh(S, subset_by_index = [len(S)-m, len(S) - 1])
    return np.diag(np.flip(v1)), np.flip(v2, axis = 1)

def get_eig_prop(S, prop):
    # Your implementation goes here!
    v1, v2 = get_eig(S, len(S))
    total = sum(np.diag(v1))
    eVal = np.diag(v1)
    #runSum = eVal[0]
    index = 0
    #print(total)
    while (prop < eVal[index]/total):
        #runSum += eVal[index+1]
        index = index + 1
    return np.diag(eVal[0:index]), v2[:, 0:index]

def project_image(image, U):
    # Your implementation goes here!
    return np.dot(np.dot(image, U), np.transpose(U))

def display_image(orig, proj):
    # Your implementation goes here!
    origRe = orig.reshape(32,32).transpose()
    projRe = proj.reshape(32,32).transpose()
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize = (13,3))
    ax1.set_title("Original")
    ax2.set_title("Projection")
    colorBarO = ax1.imshow(origRe, aspect ='equal')
    colorBarP = ax2.imshow(projRe, aspect = 'equal')
    fig.colorbar(colorBarO, ax = ax1)
    fig.colorbar(colorBarP, ax = ax2)
    plt.show()

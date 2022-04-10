import csv
import numpy
from collections import OrderedDict
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

def load_data(filepath):
    with open(filepath, newline='') as csvfile:
        dictPKMN = csv.DictReader(csvfile)
        #print(type(dictPKMN))
        listPKMN = []
        for row in dictPKMN:
            # use dict(row) to convert from orderedDict to Dict 
            # (assuming 'row' is orderedDict)
            listPKMN.append(dict(row))
        #print(type(listPKMN))
        #print(type(listPKMN[0]))
    return listPKMN

def calc_features(row):
    statPKMN = [numpy.int64(row['Attack']), numpy.int64(row['Sp. Atk']),
            numpy.int64(row['Speed']), numpy.int64(row['Defense']),
            numpy.int64(row['Sp. Def']), numpy.int64(row['HP'])]
    #print(type(statPKMN[0]))
    return numpy.array(statPKMN)

def calc_comp_link(features, c1, c2):
    newMax = -1
    for elem1 in c1:
        for elem2 in c2:
            tempDist = numpy.linalg.norm(features[elem1] - features[elem2])
            if(tempDist > newMax):
                newMax = tempDist
    return newMax

def hac(features):
    sizeFeat = len(features)
    result = numpy.zeros((sizeFeat-1, 4))
    dictIndex = {}
    ref_id = {}
    for val in range(sizeFeat):
        dictIndex[val] = [val]
        ref_id[val] = val
    #print(dictIndex)
    # create a distance matrix using nested for loop & init values
    distances = numpy.ones((sizeFeat, sizeFeat))*numpy.Inf
    for val1 in range(sizeFeat):
        for val2 in range(val1+1, sizeFeat):
                distances[val1][val2] = numpy.linalg.norm(features[val1] - features[val2])
    #print(distances)
    # start clustering and update matrix,dictClus
    for itera in range(sizeFeat - 1):
        # find min distance
        result[itera][2] = numpy.min(distances)
        # find z0, z1 of ith iteration and store it
        z01 = numpy.unravel_index(numpy.argmin(distances), distances.shape)
        #print(z01)
        # put smaller val in z0, larger in z1
        result[itera][0] = ref_id[z01[0]]
        result[itera][1] = ref_id[z01[1]]
        # merge the clusters
        # order of deletes matter
        dictIndex[sizeFeat + itera] = dictIndex[ref_id[z01[0]]] + dictIndex[ref_id[z01[1]]]
        del dictIndex[ref_id[z01[0]]]
        del dictIndex[ref_id[z01[1]]]
        ref_id[z01[0]] = sizeFeat + itera
        del ref_id[z01[1]]
        #print(dictIndex)
        #print(ref_id)
        # update distance matrix
        for a in range(sizeFeat):
            # set row & cols of z0 and z1 to inf
            distances[z01[1]][a] = numpy.Inf
            distances[a][z01[1]] = numpy.Inf
            distances[z01[0]][a] = numpy.Inf
            distances[a][z01[0]] = numpy.Inf
        for b in ref_id.keys():
            if(sizeFeat+itera != ref_id[b]):
                if(z01[0] < b):
                     distances[z01[0]][b] = calc_comp_link(features, dictIndex[sizeFeat+itera], dictIndex[ref_id[b]])
                else:
                    distances[b][z01[0]] = calc_comp_link(features, dictIndex[sizeFeat+itera], dictIndex[ref_id[b]])
        #print(distances)
        # update dictIndex
        result[itera][3] = len(dictIndex[sizeFeat + itera])
        #print(itera)
        #print(z01[0])
        #print(result)
        #print(dictIndex[ref_id[z01[0]]])
        #print(dictIndex)
    return result


def imshow_hac(Z):
    plt.figure()
    dn = hierarchy.dendrogram(Z)
    plt.show()

def main():
    listPKMNs = load_data('Pokemon.csv')
    #print(listPKMNs)
    #print(calc_features(listPKMNs[0]))
    #print(calc_features(listPKMNs[0]).shape)
    listPKMN = []
    for i in range(30):
        listPKMN.append(calc_features(listPKMNs[i]))
    Z = hac(listPKMN)
    imshow_hac(Z)
    #print(Z)

if __name__ == "__main__":
    main()
    #Z = hac([calc_features(row) for row in load_data('Pokemon.csv')][:30])
    #Z = hierarchy.linkage([calc_features(row) for row in load_data('Pokemon.csv')][:30], 'complete')
    #imshow_hac(Z)

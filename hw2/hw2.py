import sys
import math
from decimal import *

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    #X = dict()
    X = {}
    for i in range(26):
        X[chr(i + ord('A'))] = 0

    with open (filename,encoding='utf-8') as f:
        # TODO: add your code here
        for line in f:
            for i in line.strip().upper():
                if i >= 'A' and i <= 'Z':
                    X[i] += 1
        f.close()

    for i in X.keys():
        print(i, X[i])
    return X

# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!

def identify(english, spanish, dict):
    index = 0
    #sum = 0
    #cdenom = 1.0
    probE = 0.0
    probS = 0.0
    for key in dict.keys():
        #sum += dict[key]
        #cdenom *= math.factorial(dict[key])
        probE += (math.log(english[index])*dict[key])
        probS += (math.log(spanish[index])*dict[key])
        index += 1
    #C = Decimal(math.factorial(sum))/Decimal(cdenom)
    #denomE = probE * float(C) * .6 
    #denomS = probS * float(C) * .4
    #denom = denomE + denomS
    #numE = probE * float(C) * .6
    #numS = probS * float(C) * .4
    probE += math.log(.6)
    probS += math.log(.4)
    prob = -1
    if((probS - probE) >= 100):
        prob = 0
    elif((probS - probE) <= -100):
        prob = 1
    else: 
        prob = 1/(1 + (math.e**(probS - probE)))

    print("Q2")
    print("{:.4f}".format(dict['A']*math.log(english[0]),4))
    print("{:.4f}".format(dict['A']*math.log(spanish[0]),4))

    print("Q3")
    print("{:.4f}".format(probE,4))
    print("{:.4f}".format(probS,4))

    print("Q4")
    print("{:.4f}".format(prob,4))

def main():
    e,s = get_parameter_vectors()
    print("Q1")
    X = shred('samples/letter2.txt')
    
    identify(e, s, X)

if __name__ == "__main__":
    main()

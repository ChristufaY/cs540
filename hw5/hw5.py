import sys
import csv
import numpy
import matplotlib.pyplot as plt
import pandas as pd
def main():
    data = pd.read_csv(sys.argv[1])
    #print(data)
    x = []
    y = []
    for i in range(numpy.int(data.size/2)):
        x.append(data.iat[i, 0])
        y.append(data.iat[i, 1])
    #print(years)
    #print(days)
    plt.plot(x, y)
    plt.xlabel("Year")
    plt.ylabel("Number of frozen days")
    #plt.show()
    
    #Q3a
    X = numpy.ones((numpy.int(data.size/2), 2)).astype(numpy.int64)
    for val in range(numpy.int(data.size/2)):
        X[val][1] = int(x[val])
    print("Q3a:")
    print(X)

    #Q3b
    Y = numpy.array(y).astype(numpy.int64)
    print("Q3b:")
    print(Y)

    #Q3c
    Z = numpy.dot(numpy.transpose(X), X)
    print("Q3c:")
    print(Z)

    #Q3d
    I = numpy.linalg.inv(Z)
    print("Q3d:")
    print(I)

    #Q3e
    PI = numpy.dot(I, X.T)
    print("Q3e:")
    print(PI)

    #Q3f
    hat_beta = numpy.dot(PI, Y)
    print("Q3f:")
    print(hat_beta)

    #Q4
    x_test = 2021
    y_test = hat_beta[0] + hat_beta[1]*x_test
    print("Q4: " + str(y_test))

    #Q5a & Q5b
    if (hat_beta[1] < 0):
        print("Q5a: <")
        print("Q5b: Number of days that Lake Mendota is frozen during the winter,"
             + " is decreasing as years progress.")
    elif (hat_beta[1] == 0):
        print("Q5a: =")
        print("Q5b: Number of days that Lake Mendota is frozen during the winter,"
             + " is remaing the same as years progress.")
    else:
        print("Q5a: >")
        print("Q5b: Number of days that Lake Mendota is frozen during the winter,"
             + " is increasing as years progress.")

    #Q6a & Q6b
    x_prime = -hat_beta[0]/hat_beta[1]
    print("Q6a: " + str(x_prime))

    print("Q6b: x* is very compelling because that year has already passed.")
    

if __name__ == "__main__":
    main()

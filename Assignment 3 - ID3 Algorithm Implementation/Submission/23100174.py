import numpy as np
import sys	   # Inbuilt library for handling command line arguments
import pprint  # inbuilt python library for pretty printing
import math

encodings = []
array = np.loadtxt(sys.argv[1], dtype=int, delimiter=",")
f = open(sys.argv[2], "r")
encodings = f.read()
colsAdded = []


def E(x, y):

    if x == 0 or y == 0:
        return 0
    else:
        ans = -(x / (x+y))*math.log2((x / (x+y))) - (y / (x+y))*math.log2((y / (x+y)))
        return ans


def selectRoot(table):    # A general function which gives the root node from the table passed to it
# 	find the information gain of each attrbute
# 	The attribute corresponding to the max gain is the root node

    global colsAdded
    rows = np.size(table, 0)
    cols = np.size(table, 1)
    cols = cols - 1
    indexToReturn = 0
    maxIG = 0
    entropySystem = E(np.count_nonzero(table[:, -1]), rows - np.count_nonzero(table[:, -1]))

    for i in range(0, cols):

        if i in colsAdded:
            continue

        entropy = 0
        substable = table[:, [i, cols]]
        values, counts = np.unique(substable[:, 0], return_counts=True)  #For finding out unique values inside an attribute

        for j in range(0, len(values)):
            labels = np.where(substable[:, 0] == values[j])
            finalTable = substable[labels]
            numberOfYes = np.count_nonzero(finalTable[:, -1])
            numberOfNo = np.size(finalTable, 0) - numberOfYes
            entropy = entropy + (counts[j]/rows)*E(numberOfYes, numberOfNo)

        IG = entropySystem - entropy

        if IG > maxIG:
            maxIG = IG
            indexToReturn = i

    return indexToReturn

def Tree(dataset):  	# A helper function which takes in the initial dataset and repeatdely
#	finds the root node
#   dictionary[node]= {}												# calls selectRoot to construct the dictionary
#	constructs subtables for each unique class inside the root node
#	check purtity of the subtable
#	if unpure repeat the process

    global colsAdded
    newRoot = selectRoot(dataset)
    colsAdded.append(newRoot)

    values, counts = np.unique(dataset[:, newRoot], return_counts=True)
    dict = {}

    for i in range(0, len(values)):
        labels = np.where(dataset[:, newRoot] == values[i])            #For constructing a subtable
        subtable = dataset[labels]
        numberOfYes = np.count_nonzero(subtable[:, -1])

        if numberOfYes == counts[i]:
            dict[encodings.split()[newRoot+1].split(',')[i]] = "Yes"

        elif numberOfYes == 0:
            dict[encodings.split()[newRoot+1].split(',')[i]] = "No"

        else:
            colsAddedCOPY = colsAdded.copy()
            dict[encodings.split()[newRoot+1].split(',')[i]] = Tree(subtable)
            colsAdded.clear()
            colsAdded = colsAddedCOPY.copy()

    dict2 = {}
    dict2[encodings.split()[0].split(',')[newRoot]] = dict
    return dict2


pprint.pprint(Tree(array))
import anytree
import csv
import os
import sys
import collections
import math

from anytree.exporter import DotExporter
from anytree import Node, RenderTree


# read_data reads in the input examples.
def read_data(filepath: str):
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    examples = []
    features = []
    featureIndex = dict()
    headerRemoved = False
    with open(filepath) as fp:
        for line in fp:

            # Parse row and convert it to float
            row = line.split(",")
            if not headerRemoved:
                i = 0
                for col in row:
                    features.append(col)
                    featureIndex[col] = i
                    i += 1

                headerRemoved = True
                features = features[:-1]
                continue

            floatRow = []
            for col in row:
                floatRow.append(float(col))

            examples.append(floatRow)

    return (examples, features, featureIndex)


class Classifier:
    def __init__(self):
        pass

    # print_tree prints the tree to a file provided.
    def print_tree(self, path, debug = False):
        pass

    # learn_dt creates a decision tree for the data fed into the  classifier.
    def learn_dt(self):
        pass

    # predict predicts the political leaning  based on  an example profile.
    def predict(self, example):
        pass

    # get_prediction_accuracy returns the prediction accuracy of the tree on the
    # test set provided.
    def get_prediction_accuracy(self, test_set):
        pass


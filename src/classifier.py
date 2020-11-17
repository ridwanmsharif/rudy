import anytree
import csv
import os
import sys
import collections
import math

from anytree.exporter import DotExporter
from anytree import Node, RenderTree

from sklearn import tree
import graphviz


# read_data reads in the input examples.
def read_data(filepath: str):
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    examples = []
    features = []
    labels = []
    featureIndex = dict()
    headerRemoved = False
    with open(filepath) as fp:
        for line in fp:

            # Parse row and convert it to float
            row = line.strip("\n").split(",")
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
            lenRow = len(row)
            for i, col in enumerate(row):
                if i == lenRow - 1:
                    labels.append(col)
                    break

                floatRow.append(float(col))

            examples.append(floatRow)

    return (examples, labels, features, featureIndex)


class Classifier:
    def __init__(self, filepath: str, features):
        self.examples, self.labels, _, self.featuresIndex = read_data(filepath)
        self.tree = tree.DecisionTreeClassifier()
        self.features = features
        return

    # print_tree prints the tree to a file provided.
    def print_tree(self, path, debug = False):
        dot_data = tree.export_graphviz(self.tree, out_file=None,
                                        feature_names=self.features,
                                        class_names=["democrat", "republican"])
        graph = graphviz.Source(dot_data)
        graph.render(path)
        return

    # learn_dt creates a decision tree for the data fed into the  classifier.
    def learn_dt(self):
        self.tree =  self.tree.fit(self.examples, self.labels)
        return

    # predict predicts the political leaning  based on  an example profile.
    def predict(self, example):
        return  self.tree.predict(example)[0]

    # get_prediction_accuracy returns the prediction accuracy of the tree on the
    # test set provided.
    def get_prediction_accuracy(self, test_examples, test_labels):
        total = len(test_set)
        correct = 0

        for i, row in enumerate(test_examples):
            if int(test_labels[i]) == int(self.predict(row)):
                correct  += 1

        return (correct/total)*100

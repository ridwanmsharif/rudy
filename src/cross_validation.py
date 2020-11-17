from classifier import Classifier
from math import ceil
from matplotlib import pyplot as plt
from random import shuffle
from sklearn import tree as dt


def split_examples(examples, labels, k):
    # Randomize the data
    data = list(zip(examples, labels))
    shuffle(data)

    split_data = [[] for i in range(k)]

    for i, data_point in enumerate(data):
        split_data[i % k].append(data_point)

    training_data = []
    test_data = []

    for i, test_set in enumerate(split_data):
        ith_training_set = []
        for j, training_set in enumerate(split_data):
            if i == j:
                continue
            ith_training_set += training_set
        training_data.append(ith_training_set)
        test_data.append(test_set)

    return training_data, test_data


class KFold(Classifier):
    def __init__(self, k, file_path, topics):
        super(KFold, self).__init__(file_path, topics)
        self.k = k        
        training_data, test_data = split_examples(self.examples, self.labels, self.k)
        self.training_data = training_data
        self.test_data = test_data

    def get_prediction_accuracy_v2(self, test_examples):
        total = len(test_examples)
        correct = 0

        for i, row in enumerate(test_examples):
            if row[1] == self.predict(row[0]):
                correct  += 1

        return (correct/total) * 100
    
    def learn_dt_v2(self, data):
        examples, labels = zip(*data)
        self.tree =  self.tree.fit(examples, labels)

    def calculate_accuracy(self, data):
        total = sum(data)
        amount = len(data)
        return total/amount
    
    def cross_validate(self):
        raise Exception("You need to implement this")


class MaxDepth(KFold):
    def __init__(self, k, max_depth_range, file_path, topics):
        super(MaxDepth, self).__init__(k, file_path, topics)
        self.max_depth_range = max_depth_range
    
    def cross_validate(self):
        train_accuracies = []
        test_accuracies = []

        for i in self.max_depth_range:
            self.tree = dt.DecisionTreeClassifier(max_depth=i)
            k_train_accuracies = []
            k_test_accuracies = []

            for j in range(len(self.training_data)):
                self.learn_dt_v2(self.training_data[j])
                k_train_accuracies.append(self.get_prediction_accuracy_v2(self.training_data[j]))
                k_test_accuracies.append(self.get_prediction_accuracy_v2(self.test_data[j]))

            train_accuracies.append(self.calculate_accuracy(k_train_accuracies))
            test_accuracies.append(self.calculate_accuracy(k_test_accuracies))
        
        return train_accuracies, test_accuracies
        
    def plot(self, train_accuracies, test_accuracies, output_path):
        fig = plt.figure(1)
        plt.plot(self.max_depth_range, train_accuracies)
        plt.plot(self.max_depth_range, test_accuracies)
        fig.suptitle('Training and Validation Accuracy vs Max Depth')
        plt.xlabel('Max Depth')
        plt.ylabel('Accuracy')
        plt.legend(['Training Accuracy', 'Validation Accuracy'])
        fig.savefig(output_path)


class MinSamples(KFold):
    def __init__(self, k, min_samples_range, file_path, topics):
        super(MinSamples, self).__init__(k, file_path, topics)
        self.min_samples_range = min_samples_range
    
    def cross_validate(self):
        train_accuracies = []
        test_accuracies = []

        for i in self.min_samples_range:
            self.tree = dt.DecisionTreeClassifier(min_samples_split=i)
            k_train_accuracies = []
            k_test_accuracies = []

            for j in range(len(self.training_data)):
                self.learn_dt_v2(self.training_data[j])
                k_train_accuracies.append(self.get_prediction_accuracy_v2(self.training_data[j]))
                k_test_accuracies.append(self.get_prediction_accuracy_v2(self.test_data[j]))

            train_accuracies.append(self.calculate_accuracy(k_train_accuracies))
            test_accuracies.append(self.calculate_accuracy(k_test_accuracies))
        
        return train_accuracies, test_accuracies
        
    def plot(self, train_accuracies, test_accuracies, output_path):
        fig = plt.figure(2)
        plt.plot(self.min_samples_range, train_accuracies)
        plt.plot(self.min_samples_range, test_accuracies)
        fig.suptitle('Training and Validation Accuracy vs Min Samples Split')
        plt.xlabel('Min Samples Split')
        plt.ylabel('Accuracy')
        plt.legend(['Training Accuracy', 'Validation Accuracy'])
        fig.savefig(output_path)

def get_graphs(k, depths, samples, topics, examples_path, depth_path, samples_path, tree_max_depth_path, tree_min_samples_path):
    def get_best_parameter(test_data):
        best_index, best_value = 0, 0
        for i, v in enumerate(test_data):
            if v > best_value:
                best_value = v
                best_index = i
        return best_index, best_value

    md = MaxDepth(k, [i for i in range(1, 12)], examples_path, topics)
    train, test = md.cross_validate()
    index, val = get_best_parameter(test)
    print("Best Max Depth", index + 1, val)
    max_depth = index + 1
    md.plot(train, test, depth_path)

    ms = MinSamples(k, [i for i in range(2, 41)], examples_path, topics)
    train, test = ms.cross_validate()
    index, val = get_best_parameter(test)
    print("Best Min Samples Split", index + 2, val)
    min_samples = index + 2
    ms.plot(train, test, samples_path)

    classifier = Classifier(examples_path, topics)
    classifier.tree = dt.DecisionTreeClassifier(max_depth=max_depth)
    classifier.learn_dt()
    classifier.print_tree(tree_max_depth_path)

    classifier.tree = dt.DecisionTreeClassifier(min_samples_split=min_samples)
    classifier.learn_dt()
    classifier.print_tree(tree_min_samples_path)

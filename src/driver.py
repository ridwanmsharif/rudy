import sys
import time
from builddataset import *
from classifier import *
from cross_validation import *

# Driver of the program
if __name__ == '__main__':
    topics = ["Democrat", "Republic", "Election Fraud", "SCOTUS", "Climate",
              "Economic", "Foreign Military", "Local Military", "COVID" ]
    if sys.argv[1] == "tweets":
        pass
    elif sys.argv[1] == "dataset":
        dataset = Dataset(topics, "src/apikey.json")
        print("Ingesting tweets")
        dataset.ingest(sys.argv[2])
        print("Saving Dataset")
        dataset.save(sys.argv[3])
    elif sys.argv[1] == "tree":
        classifier = Classifier(sys.argv[2], topics)
        classifier.learn_dt()
        classifier.print_tree(sys.argv[3])
    elif sys.argv[1] == "cross_validate":
        get_graphs(
            int(sys.argv[2]), 
            [i for i in range(1, 12)], 
            [i for i in range(2, 41)], 
            topics, 
            sys.argv[3], 
            sys.argv[4],
            sys.argv[5])
    else:
        print("unknown command")
        sys.exit(1)

import sys
import time
from builddataset import *
from classifier import *

# Driver of the program
if __name__ == '__main__':
    topics = ["a", "b", "c", "d"]
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
    elif sys.argv[1] == "depth":
        pass
    elif sys.argv[1] == "examples":
        pass
    else:
        print("unknown command")
        sys.exit(1)

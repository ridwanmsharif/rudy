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
            sys.argv[5],
            sys.argv[6],
            sys.argv[7])
    elif sys.argv[1] == "predict":
        classifier = Classifier(sys.argv[2], topics)
        classifier.learn_dt()
        classifier.print_tree(sys.argv[3])
        examples = read_data(sys.argv[4])[0]
        assert(len(examples) == 1)
        example = examples[0]
        res = classifier.predict(example)
        print()
        print("###############################")
        print("The political leaning for the user is:", res)
        print("###############################")
        print()
    else:
        print("unknown command")
        sys.exit(1)

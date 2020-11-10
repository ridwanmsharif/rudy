import sys
import time

# Driver of the program
if __name__ == '__main__':

    # We are given a filename  that is our dataset.
    assert(len(sys.argv) == 3)

    if sys.argv[2] == "full":
        full_tree(sys.argv[1])
    elif sys.argv[2] == "depth":
        cross_validation_max_depth(sys.argv[1])
    else:
        cross_validation_min_info(sys.argv[1])

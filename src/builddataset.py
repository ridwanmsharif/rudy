from sentiment import *
import time
import sys, os, csv

class Dataset:
    def __init__(self, topics, keyfile):
        self.topics = topics
        self.keyfile = keyfile
        self.profiles = dict() # Key: handle, Value: (label, {topic: (total score, count)}

    # ingests the data from the input location
    def ingest(self, filepath):
        if not os.path.isfile(filepath):
            print("File path {} does not exist. Exiting...".format(filepath))
            sys.exit()


        analyzer = Sentiment(self.keyfile)
        inputFile = open(filepath, "r")
        while True:
            info = inputFile.readline().strip("\n")

            # if line is empty, end of file is reached
            if not info:
                break

            tweeterInfo = info.split(",")
            tweeterHandle, tweeterLabel = tweeterInfo[0], tweeterInfo[1]


            numTweets = int(inputFile.readline().strip("\n"))
            profileTopicsDict = dict()
            for i in range(numTweets):
                data = inputFile.readline().strip("\n").split(",")
                text = data[0]
                discussedTopics = data[1:]

                score  = analyzer.analyze(text)
                for t in discussedTopics:
                    if t in profileTopicsDict:
                        total, count = profileTopicsDict[t]
                        profileTopicsDict[t] = (total + score,  count + 1)
                    else:
                        profileTopicsDict[t] = (score, 1)

                # Default value.
                for t in self.topics:
                    if t not in profileTopicsDict:
                        profileTopicsDict[t] = (5.0, 1)

            # All the tweets analyzed. Must create a profile for it.
            self.profiles[tweeterHandle] = (tweeterLabel, profileTopicsDict)


        inputFile.close()
        return

    # saves the dataset in the output file
    def save(self, filepath):
        outF = open(filepath, "w")
        line = ",".join(self.topics) + ",party"
        outF.write(line)
        outF.write("\n")
        for profile in self.profiles:
            label, scores = self.profiles[profile]
            scoresForTopics = []
            for topic in self.topics:
                scoresForTopics.append(scores[topic][0]/scores[topic][1])

            line  = ""
            for i in range(len(scoresForTopics)):
                if i != 0:
                    line  += ","

                line += str(scoresForTopics[i])

            line += ","
            line += label

            # write line to output file
            outF.write(line)
            outF.write("\n")

        outF.close()
        return

# s = Dataset(["a", "b", "c", "d"])
# s.ingest("input.file")
# s.save("output.file")

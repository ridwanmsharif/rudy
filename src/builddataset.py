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

        with open(filepath, "r") as f:
            for info in f:
                info = info.strip()
                data = info.split(",")

                try:
                    tweet_index = int(data[0])
                    if tweet_index not in self.profiles:
                        self.profiles[tweet_index] = (tweeterLabel, {})

                    text = data[1]
                    discussedTopics = data[2:]
                    profileTopicsDict = self.profiles[tweet_index][1]

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

                except:
                    tweeterLabel = data[1]

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

from sentiment import *
import time
import sys, os, csv

class Dataset:
    def __init__(self, topics, keyfile):
        self.topics = topics
        self.keyfile = keyfile
        self.profiles = dict() # Key: handle, Value: (label, {topic: [tweets]}

    # ingests the data from the input location
    def ingest(self, filepath):
        if not os.path.isfile(filepath):
            print("File path {} does not exist. Exiting...".format(filepath))
            sys.exit()


        analyzer = Sentiment(self.keyfile)

        with open(filepath, "r") as f:
            count = 0
            i = 0
            for info in f:
                info = info.strip()
                data = info.split(",")

                try:
                    tweet_index = int(data[0])
                    if tweet_index not in self.profiles:
                        self.profiles[tweet_index] = (tweeterLabel, {})

                    if i >= 70:
                        continue

                    text = data[1]
                    discussedTopics = data[2:]
                    profileTopicsDict = self.profiles[tweet_index][1]

                    for t in discussedTopics:
                        if t in profileTopicsDict:
                            profileTopicsDict[t] += [text]
                        else:
                            profileTopicsDict[t] = [text]

                    self.profiles[tweet_index] = (tweeterLabel,
                                                  profileTopicsDict)
                    i += 1

                except:
                    tweeterLabel = data[1]
                    count += 1
                    print("Ingested user {}".format(count))
                    i = 0

        # Now analyze the tweets in a batched way.
        analysisDict = dict() # Key: handle, Value (label, {topic: (total, count)})
        newCount = 0
        for profile in self.profiles:
            topicScore = dict()
            label, tweetsDict = self.profiles[profile]

            # Default value.
            for t in self.topics:
                topicScore[t] = (5.0, 1)

            for t in self.topics:
                textSoFar = ""
                if t not in tweetsDict:
                    tweets = []
                else:
                    tweets  = tweetsDict[t]

                print(len(tweets), t)
                for i, tweet in enumerate(tweets):
                    textSoFar += " "
                    textSoFar += tweet
                
                score = analyzer.analyze(textSoFar)
                oldTotal, oldCount = topicScore[t]
                topicScore[t] = (oldTotal + score, oldCount + 1)

            self.profiles[profile] = (label, topicScore)
            newCount += 1
            print("Analyzed user {} with profile {} and class".format(newCount,
                                                            topicScore, label))


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

import re
import time
import sys
import time
from builddataset import *
from classifier import *
from cross_validation import *
from pruner import *

from tweets import Tweets

def fetch_tweets(handle, file_path):

    twitter = Tweets(consumer_key, consumer_secret, access_key, access_secret)

    hashtags = set()
    count = 1

    with open(file_path, 'a') as f:
        f.write(handle[0])
        f.write(",")
        f.write(handle[1])
        f.write(",")
        f.write(str(count))
        f.write("\n")

        tweets = twitter.get_all_tweets(handle[0])
        f.write(str(len(tweets)))
        f.write("\n")

        for tweet in tweets:
            if hasattr(tweet, 'retweeted_status'):
                text = tweet.retweeted_status.full_text
            else:
                text = tweet.full_text
                
            text = re.sub(r"http\S+", "", text.replace('\n', ' '))
            text = text.replace(',', '')
            text = text.strip()
            if text:
                f.write(text)
            else:
                f.write("empty")
            f.write("\n")
        count += 1


# if __name__ == "__main__":
#     get_text("twitter_handles.csv")

# Driver of the program
if __name__ == '__main__':

    if sys.argv[1] == "fetch":
        handle = [sys.argv[2], "republican"]
        fetch_tweets(handle, sys.argv[3])
    elif sys.argv[1] == "prune":
        prune_tweets(sys.argv[2], sys.argv[3])

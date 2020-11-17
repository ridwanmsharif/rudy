import re
import time

from tweets import Tweets

def get_text(file_path):
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    twitter = Tweets(consumer_key, consumer_secret, access_key, access_secret)

    hashtags = set()
    handles = []

    with open(file_path) as f:
        header = True
        for line in f:
            if header:
                header = False
                continue
            data = line.split(",")
            handles.append(data[:2])

    count = 1

    with open("../resources/tweets.csv", 'a') as f:
        for handle in handles:
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

            print(f"Got tweets for {count}")            
            count += 1


# if __name__ == "__main__":
#     get_text("twitter_handles.csv")

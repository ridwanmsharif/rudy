import tweepy
import json


class Tweets:

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

    def get_all_tweets(self, screen_name):

        tweets = []
        oldest = None

        while True:
            if oldest is not None:
                new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            else:
                new_tweets = self.api.user_timeline(screen_name=screen_name, count=200)

            if len(new_tweets) == 0:
                break

            tweets.extend(new_tweets)
            oldest = tweets[-1].id - 1
            print(f"{len(tweets)} tweets downloaded so far")

        return tweets


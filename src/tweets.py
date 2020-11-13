import tweepy
import json


class Tweets:

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

    def get_all_tweets(self, screen_name):

        #initialize a list to hold all the tweepy Tweets
        tweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = self.api.user_timeline(screen_name=screen_name, count=200)

        #save most recent tweets
        tweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = tweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:

            #all subsequent requests use the max_id param to prevent duplicates
            new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

            #save most recent tweets
            tweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = tweets[-1].id - 1

            print(f"{len(tweets)} tweets downloaded so far")

        return tweets

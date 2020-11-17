import json
import time
import tweepy


class Tweets:

    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

    def get_all_tweets(self, screen_name):

        tweets = []
        oldest = None

        while True:
            try:
                if oldest is not None:
                    new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')
                else:
                    new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

                if len(new_tweets) == 0:
                    break

                tweets.extend(new_tweets)
                oldest = tweets[-1].id - 1
                print(f"{len(tweets)} tweets downloaded so far")
            except tweepy.RateLimitError:
                print("Sleeping for 15 minutes")
                time.sleep(15 * 60)
            except tweepy.TweepError as e:
                try:
                    error_code = e.message[0]['code']
                    if error_code == 130:
                        time.sleep(5 * 60)
                    else:
                        return tweets
                except:
                    return tweets
            except Exception as e:
                print(e)
                print(f"Continuing over {screen_name}")
                return tweets

        return tweets

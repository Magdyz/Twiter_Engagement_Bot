import tweepy
import time
from random import randrange, choice


# function for autherisation of API using secret keys that are in a file called auth in the same folder

def authTwitter():
    from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)
    
    consumer_key = consumer_key
    consumer_secret = consumer_secret
    access_token = access_token
    access_token_secret = access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit = True)
    
    

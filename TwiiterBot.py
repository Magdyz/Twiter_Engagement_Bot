import tweepy
import time
from random import randrange, choice
from StatusUpdate import getNews


WaitTimeForTopics = 3600     #1800
waitTimeForTweets = 50       #800
DB = []


# Two functions, one to add new tweet id's to a document and another to make sure new tweet id's aren't in the document. 
# This was very good to prevent repeated tweets. They are used in retweetTweets() and likeTweets() functions

def store_last_id(tweet_id):

    with open('lastid.txt', 'a') as fp:
        fp.write(str(tweet_id))
        fp.write('\n')

# open text file and check if tweet id exists to avoid repetition

def get_last_id(tweet_id):
    
    with open('lastid.txt') as fp:
        file = fp.read()
        for i in file:     
            if str(tweet_id) in file:
                print('passed because it was retweeted before')
                return 'passed'
        else:
            print('Repeated tweet, skipping!')
            return 'not passed'


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
    
# retweet function with filters to remove retweets and replies using -filter and conditions
# for number of followers, to select popular accounts and a counter to control how many retweets

def retweetTweets(numberOfTimes):
    numberOfTweets = 500       # number of results
    counter=0                  # counter to control number of results everytime the function runs
    minimumFollowerCount = 10000  # the minimum number of followers for the retweet's auther
    
    tweets = tweepy.Cursor(api.search_tweets,q=searchWord()+' filter:images -filter:retweets -filter:replies -filter:hashtags -filter:mentions',
                           lang="en",tweet_mode="extended").items(numberOfTweets) # The number of tweets to return after every search.
# iterate through tweets and if user friends are above a certain number it retweets
    try:
        for tweet in tweets:
            if tweet.user.followers_count < minimumFollowerCount: 
                print('Low followers number!')
                pass                                      # a condition to skip accounts with low following
            elif counter >= numberOfTimes:
                print(counter)
                break                                     # a counter that controls how many tweets to return
            elif get_last_id(tweet.id) != 'passed':
                print('New tweet. Not retweeted before!')
                pass                                       # a condition to prevent repeated tweets by storing them 
            else:
                tweet.retweet()
# clear output verbose to explain what is happening using api tweet and tweet.user 
                counter+=1
                print ('Tweet created at: \n'+str(tweet.created_at)+ '\n\n'+f'Retweet number {count}')
                print('\nTweet text is: \n\n'+ str(tweet.full_text) + '\n')
                print('user details: \n'+'Screen name: '+str(tweet.user.screen_name)+'\nName: '+str(tweet.user.name)+' \nLocation is '+str(tweet.user.location))
                print('\nuser followers count: '+str(tweet.user.followers_count)+'\n')
                print(f'retweeted {tweet.id} successfully \n')
                store_last_id(tweet.id)
                time.sleep(1)
                print('stored successfully!')
                time.sleep(randrange(waitTimeForTweets))

# if the tweet is repeated or any error this exception is raised and stores id then pass 
    except Exception as e:
        print('Error: ' + str(e))
        print("This didn't work!") 
        store_last_id(tweet.id)
        print(f'stored this {tweet.id}')
        pass
# a function that likes tweets.

    def likeTweets():
    while True:
        tweetsFound = tweepy.Cursor(api.search_tweets,q=searchWord()+' filter:images -filter:retweets -filter:replies -follow -share -retweet -filter:hashtags -filter:mentions' ,lang="en",tweet_mode="extended").items(500)
# iterate through tweets and if user friends are above a certain number it likes it
        try:
            for tweet in tweetsFound:
                if tweet.user.followers_count < randrange(50000):
                        pass
                elif get_last_id(tweet.id) != 'passed':
                        print('passed because it was retweeted before')
                        pass
                else:
                    api.create_favorite(tweet.id)
                    print('\nuser followers count: '+str(tweet.user.followers_count)+'\n')
                    print('liked')
                    store_last_id(tweet.id)
                    time.sleep(1)
                    print('stored successfully!')
                    break
        except Exception as e:
            print('Error: ' + str(e))
            print("This didn't work!") 
            store_last_id(tweet.id)
            print(f'stored this {tweet.id}')
            pass

# main run code

while __name__ == '__main__':  

# authentication twitter API

    authTwitter()  
    api = authTwitter()
        
## UPDATE STATUS NEWS API FUNCTION ##

    api.update_status(getNews(searchWord(),skipCount))
    print('result number: '+str(skipCount))
    print('Status has been updated with News successfully')
    time.sleep(randrange(WaitTimeForTopics))
    
## LIKE TWEETS ##

    likeTweets()
    print('End of like Action!')
    time.sleep(randrange(WaitTimeForTopics))

## RETWEET FUNCTION ##

    retweetTweets(5)
    print('End of Retweet Action!')
    time.sleep(randrange(WaitTimeForTopics))

# iterate through news for all APIs
    print(f'End of loop number {skipCount+1}')
    skipCount+=1
    time.sleep(randrange(50))


 

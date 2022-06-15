
My main plan was to create a Bot that retweets interesting posts that match a certain criteria of keywords, hashtags or maybe sentences. I embarked on this journey propelled by a genuine need for engagement on my sad NFT twitter account instead of being silent, which might put my followers off. I also did it for the fun of learning to work with APIs and automation.

Here's how I did it! 

To start my connection to twitter API, I had to get access keys which are available when you sign up for a developer account on twitter. This was straight forward. You only need a twitter account. 

> https://developer.twitter.com/en/docs/platform-overview

Once done, these access keys are 'the key' to twitter API. To interact easily with the API you could use a python library called *Tweepy*

```
pip install tweepy
```
Check documentation:

> https://docs.tweepy.org/

I then created a folder called TwiterEngagementBot inside it I add the following files

- auth 
- twitterBot.py 
- StatusUpdate.py
- lastid.txt

In the auth file, I added the keys that I got access to after signing up for a developer account on Twitter.

```
consumer_key = "#########################"
consumer_secret = "##################################################"

access_token = "##################################################"
access_token_secret = "#############################################"
```

Then in `twitterBot.py`, which is the main code that runs the Bot, I connected the file in the following function  

```
def authTwitter():
    from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)
```
Then we need to do the Authorisation process. Here is an example from Twitter documentation of a normal POST request. 

```
POST /1.1/statuses/update.json?include_entities=true HTTP/1.1
Accept: */*
Connection: close
User-Agent: OAuth gem v0.4.4
Content-Type: application/x-www-form-urlencoded
Authorization:
OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog",
oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg",
oauth_signature="tnnArxj06cWHq44gCs1OSKk%2FjLY%3D",
oauth_signature_method="HMAC-SHA1",
oauth_timestamp="1318622958",
oauth_token="370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb",
oauth_version="1.0"
Content-Length: 76
Host: api.twitter.com

status=Hello%20Ladies%20%2b%20Gentlemen%2c%20a%20signed%20OAuth%20request%21
```

This could be done in Postman, so this is how it's done in Python

```
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
```
This will trigger later by calling this function `authTwitter()` to authenticate the Twitter API and gain access to all the calls and features.

Time for the main functions. One of the first functions I tried was the retweet function. I wanted to get a random keyword from a list of ready-made list of keywords that I chose. To achieve this, I needed a function the returns a random word from a list. `import random`

```
def searchWord():
# a list of words that will shape our choice of tweets. This could be any number of 
# keywords or hashtags.
    listOfWords = ['news', 'Art', 'new tech news', 'crypto', 'stocks news',
    'amazing art']
# by using choice() function the variable wordToSearch stores a random word
    wordToSearch = choice(listOfWords)
    print(f'The word used to search is: {wordToSearch}\n')
    return wordToSearch
```
This way I could guarantee a new search word every time the code runs. This is all optional. You could get away without using this function if you will use one word as I will show when we get to the actual request part. 

The main retweet function has developed a lot throughout the process and during testing. It started with a 
basic retweet structure

```
while True:
    api = authTwitter()

    for tweet in tweepy.Cursor(api.search_tweets,q=(f"{searchWord()} -filter:retweets -filter:replies has:images"),lang="en",since_id=date).items(randrange(5)):
        tweet.retweet()
        print (tweet.created_at, tweet.text, f'\n Retweeted next retweet in {randomise(10)}, search term {searchWord()}')
        time.sleep(randrange(10))

```

An example of request that has a query that is returned from the previous `searchWord()` and I used `-filter` to filter out results. For instance, `-filter:retweets` doesn't include retweets when considering retweets. Same for `-filter:replies` which means no replies to be retweeted. 

`has:images` is the opposite, meaning retweet posts that include pictures. `since_id=<dates>` is to specify a date. A lot more rules could be found in the [documentations](https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators).

I have had to change this after a lot of testing because another challenge was that I wanted this to only produce one retweet, and move to the next action, then when called, return a different tweet. I created a counter that gives me a chance to choose how many tweet. This is managed by a condition to control the loop by adding the desired number of tweets as an argument `numberOfTimes `.

```
def retweetTweets(numberOfTimes):
    counter=0
```
and
```
        elif counter >= numberOfTimes:
                        print(counter)
                        break
 ```

Another challenge that I faced and was such a bug was repeated retweets. Because I have specified a lot of filters and conditions, the resulting tweets aren't a lot, so you might not face this problem if your query is more general. When you try to send a request with a repeated tweet you receive an error message from twitter. To deal with this, I found a way that works for me. 

I created two more functions. One to create a text file and store all tweet ids used in it every time I retweet something. The other function, reads the file and makes sure the new tweet doesn't exist which means it's not repeated, then returns 'passed'.

```
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
```

I created an empty text file called lastid.txt to store ids in when running the retweet function. Here's the full retweet function. I have added a lot of print statments to provide me with a lot of details about the tweets I'm retweeting. You could add or remove any of the print statements. Or maybe add them in a log.

```
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

```
 
Once this was sorted and tested, creating a like function wasn't really that difficult. Spot the differences in code from the retweet function.

```
def likeTweets():
    while True:
        tweetsFound = tweepy.Cursor(api.search_tweets,q=searchWord()+' filter:images -filter:retweets -filter:replies'
 ,lang="en",tweet_mode="extended").items(500)

# iterate through tweets and if user friends are above a certain number it likes
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
```

I have used `try - except` combo to avoid any breaking because of a nasty error. This way is great to keep things running in case of errors. In the `likeTweets():` function, I chose to use a while loop to make sure the function keeps going until it finds a tweet that meets all the conditions. The two implementations work absolutely fine,either with or without a while loop. 

That's basically it for like and retweet. Here comes the fun part. APIs!

Before, I move forward, There are four variables that will be used throughout. 

```
WaitTimeForTopics = 3600         # The time between each post (like, retweet or status      change)
waitTimeForTweets = 50       # The time between each retweet in the retweetTweets finction
skipCount = 0  # skip topics for getBingNews() - check Bing News API documentations
DB = []              # a list of all tweets or status update to prevent repetition.
```

I have decided to keep all APIs in a separate file in the same folder. So, I created `StatusUpdate`. I will give an example with one API for news. You can have access to news APIs from your favourite news source or I personally used rapidapi.com.

To update twitter status you use `api.update_status()`

Rapidapi is very user-friendly. All you need to do is find the topic, choose a provider's api then choose the programming language (in our case Python), that's it. Copy the code and you're game.

Here is an example:

![screenShot.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1655315041699/PXHOSu7Py.png align="left")
      
And this is an example of my StatusUpdate file. You will need to signup to get keys for all APIs. The arguments in the API are for `keyword` (which will be used from the random function we have in our main code `searchWords()`) and `num` which is used for choosing a certain result or iterating through news.

```
import requests
import json
import time

skipCount = 0

# Get news from Rapidapi

def getBingNews(keyword,skipCount):
    try:
        url = "https://bing-news-search1.p.rapidapi.com/news/search"

        querystring = {"q":keyword,"safeSearch":"Off","offset":1,"textFormat":"Raw","originalImg":"true",
                       "freshness":"Day","setLang":"EN","sortBy":"Date","count":"100"}
    #print(skipCount)
        headers = {
                "Accept-Language": "EN",
                "X-BingApis-SDK": "true",
                "X-RapidAPI-Host": "########################",
                "X-RapidAPI-Key": "###############################"
            }
        response = json.loads((requests.request("GET", url, headers=headers,params=querystring)).text)
        print('Status is about to be updated with Bing News')
        return (response['value'][skipCount]['name']+'\n'+response['value'][skipCount]['url'])
    
    except Exception as e:
        print('Error: ' + str(e))
        print("Couldn't get Bing News!")
        pass
```
     
You will need to `import json` library in order to deal with the JSON API response. I used `json.loads()` to make the API reply in a readable Python list. 

That's basically it. I hope this has been helpful. I have learnt a lot while working on this fun project. Here are my key learnings:

 - Always use `try - except` because a program like this is designed to run on it's own so any stoppage in a functions isn't a big deal but for the code to stop that's unacceptable. 

- Using a random library in this application made everything a lot easier. Especially, knowing that Twitter doesn't like automated posting. `import random` and the methods `choice` and `randrange` were used extensively throughout.

- lastly, testing the app many times helped me identify problems like repetition error and other bugs.

I still need to work on testing module for this, so stay tuned and follow my github repo. 

[Github repository](https://github.com/Magdyz/TwiiterEngagementBot)

Happy to answer any questions. Please post them below.
Happy Coding!

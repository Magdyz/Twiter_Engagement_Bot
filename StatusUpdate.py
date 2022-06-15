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


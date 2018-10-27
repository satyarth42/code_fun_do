from django.http import JsonResponse, HttpResponse
import pandas as pd
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
import tweepy
from tweepy import OAuthHandler
import json
import requests
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import Tree
import nltk
import numpy as np


CycloneLatitude = []
VolcanoLatitude = []
FloodLatitude = []
EarthquakeLatitude = []

consumer_key = "ZtHWuNfHCWV3XqmFSuXv0FyKn"
consumer_secret = "gmgepICbMUVtnmePAa6ibcr93r89b7zzx72wfCWhonyJlbbWm7"
access_token = "151769085-yx4BQMhM3rrRnZ7B7pnWcXwVIBu2uXwx8AD3vigc"
access_token_secret = "r969t4xTfgLigwD1oh1JHkv91ArYUMNmry7MDnGyEsKOk"
news_api_key = "0caac5d3c8d1407dbaac793cba1f1b19"
locationAppID = "fdx72S7zGbSDCbyrucgD"
locationAppCode = "zY-u6Se4lKX6UzKz5qb9pQ"


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

data = pd.read_csv('C:\\Users\\persy\\Desktop\\database.csv', encoding='latin-1')


def distance(lat1, lat2, lon1, lon2):
    lon1 = np.radians(lon1)
    lon2 = np.radians(lon2)
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2

    c = 2 * np.arcsin(np.sqrt(a))

    r = 6371

    return (c * r)


def estimation(weights, magnitude, k):
    k_weights = 1 / (weights[:k])
    k_magnitude = magnitude[:k]

    for i in range(k):
        if weights[i] > 8000.0:
            k_magnitude[i] /= 5

    prediction = np.sum((k_magnitude * k_weights)) / (np.sum(k_weights))

    return prediction


# Function to get Magnitude

def get_magnitude(MyJsonList):
    mylist = []
    for i in MyJsonList:
        coord = data.loc[:, ['Latitude', 'Longitude']]
        magnitude = data['Magnitude']
        X = coord.values
        Y = magnitude.values

        lat = i['Latitude']
        long = i['Longitude']

        dist_coord = distance(lat, long, X[:, 0], X[:, 1])

        weights = np.array([y for y, x in sorted(zip(dist_coord, magnitude))])
        magnitude = np.array([x for y, x in sorted(zip(dist_coord, magnitude))])
        myjson = {}
        myjson['Magnitude'] = estimation(weights, magnitude, 10)
        myjson['Latitude'] = i['Latitude']
        myjson['Longitude'] = i['Longitude']
        myjson['Location'] = i['Location']
        mylist.append(myjson)

    return mylist


# Function to get Latitude and Longitude from Location

def get_latitude(CycloneLocation):
    CycloneLatitude = []

    for i in CycloneLocation:
        LatitudeJson = requests.get("https://geocoder.api.here.com/6.2/geocode.json?app_id=" + locationAppID + "&app_code=" + locationAppCode + "&searchtext=" + i)
        LatitudeJson =LatitudeJson.json()
        LatitudeJson = LatitudeJson['Response']
        try:
            LatitudeJson = LatitudeJson['View'][0]
            LatitudeJson = LatitudeJson['Result'][0]
            LatitudeJson = LatitudeJson['Location']
            LatitudeJson = LatitudeJson['DisplayPosition']
            latitude = LatitudeJson['Latitude']
            longitude = LatitudeJson['Longitude']
            #['View']['Result']['Location']['DisplayPosition']['Latitude']
            #print("yo")
            #longitude = LatitudeJson['Response']['View']['Result']['Location']['DisplayPosition']['Longitude']
            MyJson = {}
            MyJson['Latitude'] = latitude
            MyJson['Longitude'] = longitude
            MyJson['Magnitude'] = None
            MyJson['Location'] = i
            CycloneLatitude.append(MyJson)
        except:
            CycloneLatitude = CycloneLatitude

    return CycloneLatitude



# Function to get location from Text

def get_location(text, label="GPE"):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == label:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk


# Function for cleaning tweets

def cleantweet(tweets, do):
    cleaned_tweets = []
    for i in tweets:
        result = re.sub(r"http\S+", " ", i)
        result = re.sub(r"(@[A-Za-z0-9]+)", " ", result)
        result = re.sub(r"[^a-zA-z]", " ", result)
        result = re.sub('rt', " ", result)
        result = result.lower().split()
        if do == 1:
            result = [ps.stem(word) for word in result if not word in mystopwords]
        result = ' '.join(result)
        cleaned_tweets.append(result)
    return cleaned_tweets


# Data_preprocessing
Datasets = pd.read_csv('C:\\Users\\persy\\Desktop\\socialmedia-disaster-tweets-DFE.csv', encoding='latin-1')

y = []
for i in Datasets['choose_one']:
    if i == 'Relevant':
        y.append(1)
    else:
        y.append(0)

X = Datasets['text']

nltk.download('stopwords')

ps = PorterStemmer()
corpus = []
mystopwords = set(stopwords.words('English')) - set('not')
for i in X:
    result = re.sub(r"http\S+", " ", i)
    result = re.sub(r"(@[A-Za-z0-9]+)", " ", result)
    result = re.sub(r"[^a-zA-z]", " ", result)
    result = result.lower().split()
    result = [ps.stem(word) for word in result if not word in mystopwords]
    result = ' '.join(result)
    corpus.append(result)

classifier = GaussianNB()
cv = CountVectorizer(max_features=1200)
X = cv.fit_transform(corpus).toarray()
classifier.fit(X, y)

def index(request):
    if request.method == "GET":
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        # Earthquake Tweets from Twitter
        tweets = []
        fetched_tweets = api.search(q="earthquake", count=100)
        for tweet in fetched_tweets:
            tweets.append(tweet.text)

        cleaned_tweets = cleantweet(tweets, 1)

        EarthquakeTweets = cleantweet(tweets, 0)

        transformed = cv.transform(cleaned_tweets).toarray()
        transformed = classifier.predict(transformed)
        EarthquakeRelevant = transformed.tolist()

        RelevantEarthquakeTweets = []

        for u in range(len(EarthquakeRelevant)):
            if str(EarthquakeRelevant[u])=='1':
                RelevantEarthquakeTweets.append(EarthquakeTweets[u])

        # Flood Tweets from Twitter

        tweets = []
        fetched_tweets = api.search(q="flood", count=100)
        for tweet in fetched_tweets:
            tweets.append(tweet.text)

        cleaned_tweets = cleantweet(tweets, 1)
        FloodTweets = cleantweet(tweets, 0)

        transformed = cv.transform(cleaned_tweets).toarray()
        transformed = classifier.predict(transformed)
        FloodRelevant = transformed.tolist()

        RelevantFloodTweets = []

        for u in range(len(FloodRelevant)):
            if str(FloodRelevant[u]) == '1':
                RelevantFloodTweets.append(FloodTweets[u])

        # Volcano Eruption Tweets from Twitter

        tweets = []
        fetched_tweets = api.search(q="valcano", count=200)
        for tweet in fetched_tweets:
            tweets.append(tweet.text)

        cleaned_tweets = cleantweet(tweets, 1)

        VolcanoTweets = cleantweet(tweets, 0)

        transformed = cv.transform(cleaned_tweets).toarray()
        transformed = classifier.predict(transformed)
        VolcanoRelevant = transformed.tolist()

        RelevantVolcanoTweets = []

        for u in range(len(VolcanoRelevant)):
            if str(VolcanoRelevant[u]) == '1':
                RelevantVolcanoTweets.append(VolcanoTweets[u])

        # Cyclone Tweets from Twitter

        tweets = []
        fetched_tweets = api.search(q="cyclone", count=200)
        for tweet in fetched_tweets:
            tweets.append(tweet.text)

        cleaned_tweets = cleantweet(tweets, 1)
        CycloneTweets = cleantweet(tweets, 0)
        for i in CycloneTweets:
            print(i)

        transformed = cv.transform(cleaned_tweets).toarray()
        transformed = classifier.predict(transformed)
        CycloneRelevant = transformed.tolist()

        RelevantCycloneTweets = []

        for u in range(len(CycloneRelevant)):
            if str(CycloneRelevant[u]) == '1':
                RelevantCycloneTweets.append(CycloneTweets[u])

        # News API Cyclone

        NewsCyclone = requests.get("https://newsapi.org/v2/everything?q=cyclone&sortBy=publishedAt&apiKey="+news_api_key)
        NewsCyclone = NewsCyclone.json()
        NewsCycloneTweets = []

        for news in NewsCyclone['articles']:
            NewsCycloneTweets.append(str(news['content']))

        # News API Earthquake
        NewsEarthquake = requests.get("https://newsapi.org/v2/everything?q=earthquake&sortBy=publishedAt&apiKey="+news_api_key)
        NewsEarthquake = NewsEarthquake.json()
        NewsEarthquakeTweets = []

        for news in NewsEarthquake['articles']:
            NewsEarthquakeTweets.append(str(news['content']))

        # News API Volcano
        NewsVolcano = requests.get("https://newsapi.org/v2/everything?q=volcano&sortBy=publishedAt&apiKey=" + news_api_key)
        NewsVolcano = NewsVolcano.json()
        NewsVolcanoTweets = []

        for news in NewsVolcano['articles']:
            NewsVolcanoTweets.append(str(news['content']))

        # News API Flood

        NewsFlood = requests.get("https://newsapi.org/v2/everything?q=flood&sortBy=publishedAt&apiKey=" + news_api_key)
        NewsFlood = NewsFlood.json()
        NewsFloodTweets = []

        for news in NewsCyclone['articles']:
            NewsFloodTweets.append(str(news['content']))

        VolcanoLocation = []

        for text in RelevantVolcanoTweets:
            my = get_location(text)
            for i in my:
                VolcanoLocation.append(i)

        for text in NewsVolcanoTweets:
            my = get_location(text)
            for i in my:
                VolcanoLocation.append(i)

        EarthquakeLocation = []

        for text in RelevantEarthquakeTweets:
            my = get_location(text)
            for i in my:
                EarthquakeLocation.append(i)

        for text in NewsEarthquakeTweets:
            my = get_location(text)
            for i in my:
                EarthquakeLocation.append(i)

        FloodLocation = []

        for text in RelevantFloodTweets:
            my = get_location(text)
            for i in my:
                FloodLocation.append(i)

        for text in NewsFloodTweets:
            my = get_location(text)
            for i in my:
                FloodLocation.append(i)

        CycloneLocation = []

        for text in RelevantCycloneTweets:
            my = get_location(text)
            for i in my:
                CycloneLocation.append(i)

        for text in NewsCycloneTweets:
            my = get_location(text)
            for i in my:
                CycloneLocation.append(i)

        for i in CycloneLocation:
            print(i)

        #https://geocoder.api.here.com/6.2/geocode.json?app_id={YOUR_APP_ID}&app_code={YOUR_APP_CODE}&searchtext=425+W+Randolph+Chicago

        global CycloneLatitude
        CycloneLatitude= get_latitude(CycloneLocation)
        global VolcanoLatitude
        VolcanoLatitude  = get_latitude(VolcanoLocation)
        global FloodLatitude
        FloodLatitude = get_latitude(FloodLocation)
        global EarthquakeLatitude
        EarthquakeLatitude = get_latitude(EarthquakeLocation)
        EarthquakeLatitude = get_magnitude(EarthquakeLatitude)

        return HttpResponse("Updated")

def getrequest(request):
    myjson = {}
    myjson['earthquake'] = EarthquakeLatitude
    myjson['cyclone'] = CycloneLatitude
    myjson['flood'] = FloodLatitude
    myjson['volcano'] = VolcanoLatitude

    return JsonResponse(myjson)

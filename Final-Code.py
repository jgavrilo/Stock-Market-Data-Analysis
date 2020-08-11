# CIS 400 Final Project
# John-Paul Besong, Dounglan Cheung, Mario Garcia, Jeremy Gavrilov, Zachary Pinter

# imports needed
import twitter
from textblob import TextBlob
import datetime
import sys
import time
import json
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt

# Company stock to observe
# For illustrative purposes, when all else fails, search for Justin Bieber
# and something is sure to turn up (at least, on Twitter)
company = 'TSLA'
stock = '$' + company
date = '2020-05-04'         # Input date in a 'year-month-day' fashion as shown 


# Twitter Login
def oauth_login():
    CONSUMER_KEY = 'q0BHmWmkkw3wdT7yAOZ8QP8hW'
    CONSUMER_SECRET = 'epqi2fnKbMEjifDfJObowDd4blQVwzE3vP3blAsiZVh9UJpQ60'
    OAUTH_TOKEN = '710158731-U8NJr0r5lzDpfFYntkgC1VFDdXoTiwfZERYqJ6ie'
    OAUTH_TOKEN_SECRET = 'KBsTEZJ8M8P1xSfj1t4EBZi1gNlN4rJRHxdxfghkxTbIv'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    return (twitter_api)

# Returns an instance of twitter.Twitter
twitter_api = oauth_login()
# Returns an instance of the twitter_stream
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
# Returns the Twitter stream filtering in all references of the company at hand
stream = twitter_stream.statuses.filter(track=stock)

print('Filtering the public timeline for track={0}'.format(stock), file=sys.stderr)
sys.stderr.flush()

# starting time
firstDT = datetime.datetime.now()
print("Start time:",str(firstDT))

# The two main variable that are ment to be taken account for in this loop are the
# total number of tweets counted and the total polarity of all tweets
totalPolarity = 0   
tweetsCounted = 0
    
for tweet in stream:
    tweetsCounted += 1
    text = tweet['text']
    print(text)
    blobText = TextBlob(text)
    polarity, subjectivity = blobText.sentiment
    totalPolarity += polarity
    if (tweetsCounted > 5):        # This value can be changed to give a more accurate prediction
        break

print("The total polarity of ", company, " is: ", totalPolarity)
if (totalPolarity > 0):
    print("Looks like the stock might go up today")
    print("Number of tweets: ", tweetsCounted)
if (totalPolarity < 0):
    print("Looks like the stock might go down today")
    print("Number of tweets: ", tweetsCounted)
if (totalPolarity == 0):
    print("Looks like the stock will stay the same same today")
    print("Number of tweets: ", tweetsCounted)


# end date time
lastDT = datetime.datetime.now()
print("End time:", str(lastDT))
print("Total Time:", str(lastDT-firstDT))

# Key for Alpha_Vantage
key = '2Z7954OEL53VNE1Z'
ts = TimeSeries(key)
aapl, meta = ts.get_daily(symbol=company)

# Print for given days stock info
print(aapl[date])

# Chose your output format, or default to JSON (python dict)
ts = TimeSeries(key, output_format='pandas')
ti = TechIndicators(key)

# Get the data, returns a tuple
# aapl_data is a pandas dataframe, aapl_meta_data is a dict
aapl_data, aapl_meta_data = ts.get_intraday(symbol=company, interval='5min')
# aapl_sma is a dict, aapl_meta_sma also a dict
aapl_sma, aapl_meta_sma = ti.get_sma(symbol=company)

# Visualization
# This plots a graph of all the closing prices of the given companies stock
figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
aapl_data['4. close'].plot()
plt.tight_layout()
plt.grid()
plt.show()

# Was originally used for testing
#filewrite = open(date+".txt", 'w')
#filewrite.write(aapl_data)
#np.savetxt(r'c:\data\np.txt',aapl_data.get_values())
#filewrite.close()



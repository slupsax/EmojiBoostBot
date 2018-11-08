# Emoji Boost Bot
#
# Giving emojis their much needed love by spamming the least used, according
# to emojitracker.com, until it is the least used.
#
# This is intended to be run once per day, but it is TBD whether that will be 
# handled in this script or on hosting server
#
# Created by Trevor Kay (@trevorkay724)
# With major help and inspiration from Least Used Emoji Bot on twitter (@leastUsedEmoji), 
# which was created by @nocturnalBadger
# Source code for that: 
# https://github.com/nocturnalbadgr/LeastUsedEmojiBot/blob/master/least_used_emoji_bot.py

from bs4 import BeautifulSoup
import tweepy
import Tkinter
import math
import requests
import json
import time

url = 'http://www.emojitracker.com/api/rankings'

# used to check if the compose_tweet function is still running
# perhaps try replacing with locks
is_tweeting = False

# some twitter stuff
consumer_key = # random string
consumer_secret = # random string
access_token = # random string
access_token_secret = # random string

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()

# gets the data for the least used emoji
def get_least_used():
    response = requests.request("GET", url)

    data = json.loads(response.text)

    return data[-1]

# gets the data for the second least used emoji
def get_next_least_used():
    response = requests.request("GET", url)

    data = json.loads(response.text)

    return data[-2]
    
# calculates the difference in usage between the two least used emojis
# and returns this as an int
def get_difference():
    return int(get_next_least_used()["score"]) - int(get_least_used()["score"])

# converts the emoji code obtained from emojitracker's json to 
# a unicode emoji that can be tweeted and used int unicode strings
def emoji_unicode(emoji_data):
    return unicode('\U000'+emoji_data["id"]).decode('unicode-escape')

# This composes the tweets to be made every day
def compose_tweets():
    is_tweeting = True
    difference = get_difference()
    least_used = emoji_unicode(get_least_used())

    # sends the initial tweet and then stores the tweet ID into twt_id for replies
    twt = api.update_status(least_used + " is currently the least used emoji. Let's fix that!")
    twt_id = twt.id_str

    # begin spamming emoji
    for x in range(0,difference):
        # send tweet with single emoji
        # emojitracker tracks how many tweets have used the emoji, not 
        # how many times the emoji has been used, so each tweet will
        # only boost by one
        twt = api.update_status(least_used, twt_id)
        twt_id = twt.id_str

        # needs to sleep to avoid getting stopped by twitter tweet limit
        if ((x % 48) == 0) and x != 0:
            print "sleeping..."
            twt = api.update_status("Taking a break, don't want to be too spammy", twt_id)
            twt_id = twt.id_str
            # 30 minutes
            time.sleep(1800)
            difference = get_difference()
            print "back on my bullshit!"

    api.update_status("hopefully that helped out " + least_used, twt_id)



print (user.name)

compose_tweets()




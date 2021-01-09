#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import tweepy
import csv

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

def analyze_status(text):
    if 'RT' in text[0:3]:
        return 0;
    else:
        return 1;
def time_analyzer(time):
    print("the tweets was created in",time)
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
      if(analyze_status(status.text)==1):
          writer.writerow([status.created_at,status.text,status.id])
          print(status.created_at,status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False



with open('UCL_match2.csv', 'w',newline='', encoding='utf-8') as tf:
    writer = csv.writer(tf, delimiter=',')
    writer.writerow(['created_at','Text','Tweet_ID' ])
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=['#ليفربول_توتنهام'])
    tf.close()









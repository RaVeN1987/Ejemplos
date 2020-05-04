#Autor: Tomás Castaño
#Descripción: Script que busca los trendings topics de España, los devuelve en una lista ordenada por número de tweets, crea un archivo chart de 
# barras horizontal y lo publica en twitter
#
#
#


# -*- coding: utf-8 -*-
import tweepy
import pandas as pd
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import re
import matplotlib.dates as mdates
         #           consumer_key = "xxxxxxxxx",
         #           access_token = "xxxxxxxxxx",
         #           consumer_secret = "xxxxxxxxxxxxx",
         #           access_secret = "xxxxxxxxxxxxx")



class TwitterBot():
    def __init__(self):
        self.consumer_key ="xxxxxxxxxxxx"
        self.acces_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        self.consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        self.access_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.acces_token, self.access_secret)
        self.colors = ['#012A36', '#00487C', '#0B4F6C', '#376996', '#3E92CC', '#556F7A', '#556F7A']
        self.datetimeLastExecution = x = datetime.datetime.now()
        self.datetimeLastExecution = x.strftime("%x")
        global api
        self.api = tweepy.API(self.auth)
        try:
            self.api.verify_credentials()
            print("ok")
        except:
            print("ko")
            
    
    def searchTweets(self, q, lang, rpp):
        tweets = self.api.search(q, lang, rpp)
        for tweet in tweets:
            print(tweet.text)
            
    def searchHashtag(self):
        dateExecutionsearchHashtag = str(datetime.date.today())
        trends_available = self.api.trends_available()
        trends_available_df = pd.DataFrame(trends_available)
        Spain_trends_available_df = trends_available_df[ (trends_available_df['country'] == 'Spain')]
        for i in Spain_trends_available_df.index:
            trends_location = self.api.trends_place(Spain_trends_available_df['woeid'][i])
            place = trends_location[0]["locations"]
            place = list(map(itemgetter('name'), trends_location[0]["locations"])) 
            place = str(place)
            place = place.strip("['']")
            hashtag1 = "#"+ place
            hashtag2 =  "#Trending"+place
           # trends_location = json.loads(trends_location)
            trends_location_df = pd.DataFrame(trends_location[0]['trends'])
           # trends_location_df = trends_location_df[trends_location_df.name.str.contains('#',case=True)]
            trends_location_df_No_Nan = trends_location_df[trends_location_df['tweet_volume'].notna()]
            trends_location_df_No_Nan = trends_location_df_No_Nan.sort_values(by='tweet_volume', ascending=False)
            trends_location_df_No_Nan = trends_location_df_No_Nan.reset_index()
            try:
                texts = ("Top Trending Topics ahora mismo en " + place + ":" + '\n' + 
                trends_location_df_No_Nan["name"][0] + '\n' + 
                trends_location_df_No_Nan["name"][1] + '\n' +
                trends_location_df_No_Nan["name"][2] + '\n' + 
                trends_location_df_No_Nan["name"][3] + '\n' + 
                trends_location_df_No_Nan["name"][4] + '\n' +
                hashtag1 + " " + hashtag2)
                result= "ok"
            except:
                result = "error"
                print("error")
                
            trends_location_df_No_Nan = trends_location_df_No_Nan.head(10)
            print(texts)
            plt.rcdefaults()
            fig, ax = plt.subplots()
            # Axis formatting.
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['bottom'].set_color('#DDDDDD')
            ax.tick_params(bottom=False, left=False)
            ax.set_axisbelow(True)
            ax.yaxis.grid(True, color='#EEEEEE')
            ax.xaxis.grid(False)
            y_pos = np.arange(len(trends_location_df_No_Nan["name"]))
            ax.barh(y_pos, trends_location_df_No_Nan["tweet_volume"], align='center', color = self.colors)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(trends_location_df_No_Nan["name"])
            ax.invert_yaxis()  # labels read top-to-bottom
            ax.set_xlabel('Tweets')
            ax.set_title("Trending Topics ahora mismo en " + place)
            #trends_location_df_No_Nan = int(trends_location_df_No_Nan["tweet_volume"])
            #trends_location_df_No_Nan = twitwerbot.remove_zeros(trends_location_df_No_Nan["tweet_volume"])
            for index, value in enumerate(trends_location_df_No_Nan["tweet_volume"]):
                plt.text(value, index, int(value))
            filename = "TrendingTopic"+ place + dateExecutionsearchHashtag +".png"
            SavePath = "/home/tomas/Proyectos/Python/Twitter/Graficos/Trendings/"
            plt.savefig(SavePath + filename, bbox_inches='tight')
            self.api.update_with_media(filename=SavePath+filename, status= texts)
            time.sleep(50)
            plt.show()
            plt.close() 


twitwerbot = TwitterBot()
twitwerbot.searchHashtag()

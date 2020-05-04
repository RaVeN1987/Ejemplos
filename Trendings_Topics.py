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





    def CoronaTotalDataGlobal(self):
        SpainData = {"Comunidad" :["Andalucia", "Aragón", "Asturias", "Islas Baleares", "Canarias","Cantabria","Castilla la Mancha","Castilla León","Cataluña","Ceuta","Valencia","Extremadura","Galicia","Comunidad de Madrid","Melilla","Murcia","Navarra","País Vasco","La Rioja"],
                     "Poblacion" :[8409738, 1324397, 1028244, 1150839 , 2127685, 580229, 2106331,	2418694, 7619494,84777,794288,1067710,2708339,6661949, 86487, 453258, 647554, 2167707,315675],
                     "Partido" :["PP","PSOE","PSOE","PSOE","PSOE","PRC","PSCM-PSOE","PP","JxCat","PP","Compromis","PSOE","PP","PP","C's","PP","PSN-PSOE","EAJ-PNV","PSOE"],
                     "CCAA" :["AN","AR","AS","IB","CN","CB","CM","CL","CT","CE","VC","EX","GA","MD","ML","MC","NC","PV","RI"]
                     }
                         
        SpainDataFrame = pd.DataFrame(SpainData, columns=["Comunidad","Poblacion","Partido","CCAA"])
        
        data = pd.read_csv("https://covid19.isciii.es/resources/serie_historica_acumulados.csv", encoding = "ISO-8859-1")
        data = data[1:-6]
        data[["CASOS","Hospitalizados","UCI","Fallecidos","Recuperados"]] = data[["CASOS","Hospitalizados","UCI","Fallecidos","Recuperados"]].fillna(0)
        #Union de los do dataframes
        dataJoin = pd.merge(SpainDataFrame, data, on="CCAA")
        sum(dataJoin["CASOS"])
        databyDate = data.groupby('FECHA', as_index=False)['CASOS','Hospitalizados',"UCI","Fallecidos","Recuperados"].sum().reset_index(drop=True)
        databyDate['FECHA'] = pd.to_datetime(databyDate['FECHA'], format='%d/%m/%Y')
        databyDate = databyDate.sort_values(by='FECHA', ascending=True)
        databyDate = databyDate.reset_index(drop=True)
        size = len(databyDate.index)
        InitDate = str(databyDate["FECHA"].min())
        lastDate = str(databyDate["FECHA"].max())
        PrevLast = str(databyDate["FECHA"][size-2])
        #Creamos los dos dataSets
        Databydayyesterday = databyDate[databyDate.FECHA == lastDate]
        DatabydayTwodaylast = databyDate[databyDate.FECHA == PrevLast]
        DatabydayTwodaylast.reset_index(drop=True)
        Databydayyesterday.reset_index(drop=True)
        result = Databydayyesterday.subtract(DatabydayTwodaylast.squeeze())
        result = result.reset_index(drop=True)
        result["CASOS"] = result["CASOS"].astype(int).astype(str)
        result["Hospitalizados"] = result["Hospitalizados"].astype(int).astype(str)
        result["UCI"] = result["UCI"].astype(int).astype(str)
        result["Fallecidos"] = result["Fallecidos"].astype(int).astype(str)
        result["Recuperados"] = result["Recuperados"].astype(int).astype(str)
        texto  = ("Evolución de los casos de Coronavirus en España en las últimas 24 horas: " + '\n' + 
                        "Nuevos Casos: " + result["CASOS"][0] + '\n' + 
                        "Hospitalizados:" + result["Hospitalizados"][0] + '\n' + 
                        "Ingresos en la UCI:" + result["UCI"][0] + '\n' +
                        "Fallecidos:" + result["Fallecidos"][0] + '\n' +
                        "Recuperados:" + result["Recuperados"][0] + '\n' +
                        "Fuente: https://covid19.isciii.es. #Coronavirus, #CoronavirusEspaña" 
                        )
        
        print(texto)
        databyDatediff = pd.DataFrame(databyDate["FECHA"] )
        databyDate["CASOS"] = databyDate["CASOS"].astype(int)
        databyDatediff["CASOS"] = databyDate["CASOS"].diff(periods=-1)
        databyDatediff["CASOS"] =(databyDatediff["CASOS"] * -1)
        databyDatediff["Hospitalizados"] = databyDate["Hospitalizados"].diff(periods=-1)
        databyDatediff["Hospitalizados"] =(databyDatediff["Hospitalizados"] *-1)
        databyDatediff["UCI"] = databyDate["UCI"].diff(periods=-1)
        databyDatediff["UCI"] =(databyDatediff["UCI"] *-1)
        databyDatediff["Fallecidos"] = databyDate["Fallecidos"].diff(periods=-1)
        databyDatediff["Fallecidos"] =(databyDatediff["Fallecidos"] *-1)
        databyDatediff["Recuperados"] = databyDate["Recuperados"].diff(periods=-1)
        databyDatediff["Recuperados"] =(databyDatediff["Recuperados"] *-1)
        type(databyDatediff["FECHA"])
        databyDatediff['FECHA'] = pd.to_datetime(databyDatediff['FECHA'], format='%d/%m/%Y')
        databyDatediff.drop(databyDatediff.tail(1).index,inplace=True) # drop last n rows
        # Import Data
        plt.rcdefaults()
        fig, ax = plt.subplots()
        fig.autofmt_xdate()
        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
        
        # Axis formatting.
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.tick_params(bottom=False, left=False)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color='#EEEEEE')
        ax.xaxis.grid(False)
        plt.plot(databyDatediff["FECHA"], databyDatediff["CASOS"], label='CASOS')
        plt.plot(databyDatediff["FECHA"], databyDatediff["Hospitalizados"], label='Hospitalizados')
        plt.plot(databyDatediff["FECHA"], databyDatediff["UCI"], label='UCI')
        plt.plot(databyDatediff["FECHA"], databyDatediff["Fallecidos"], label='Fallecidos')
        plt.plot(databyDatediff["FECHA"], databyDatediff["Recuperados"], label='Recuperados')
        plt.title('Evolución diaria de los casos de Coronavirus', fontsize=14)
        #plt.axis('equal')
        plt.legend();
        filename = "EvolucionDiariaCorona"+ lastDate + ".png"
        SavePath = "/home/tomas/Proyectos/Python/Twitter/Graficos/Corona/"
        plt.savefig(SavePath + filename, bbox_inches='tight')
        self.api.update_with_media(filename=SavePath+filename, status= texto)
        time.sleep(50)
        plt.show()






twitwerbot = TwitterBot()
twitwerbot.searchHashtag()

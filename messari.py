
from asyncio.windows_events import NULL

import urllib
import datetime
from datetime import timezone, datetime
import requests
import json

API_KEY = '114a9365-dbc2-4336-b212-aa7919f56483'


class Messari():

    def __init__(self, secret):

        self.__apiSecret = secret

    def __sendRequest(self, path):

        endpoint = 'https://data.messari.io/api/' + path

        response = requests.get(endpoint, params = dict(key= self.__apiSecret))

        return response


    def getAssetsData(self, version, limit):

        path = version + "/assets?limit=" + str(limit)

        response = self.__sendRequest(path).json()

        assets = {}

        for i in response['data']:

            assets[i['symbol']] = i

        return assets

       
    def getAssets(self, version, limit):

        assetsData = self.getAssetsData(version, limit)

        assets = list(assetsData.keys())

        return assets


    def getMarketCap(self, version,limit):

        path = version + "/assets?limit=" + str(limit)

        response = self.__sendRequest(path).json()

        assets = {}

        for i in response['data']:

            aux = i['metrics']['marketcap']

            assets[i['symbol']]={'rank':aux['rank'],'marketcap_dominance_percent':aux['marketcap_dominance_percent'],'current_marketcap_usd':aux['current_marketcap_usd']}

        return assets


    def getMarketData(self, version,limit):

        path = version + "/assets?limit=" + str(limit)

        response = self.__sendRequest(path).json()

        assets = {}


        for i in response['data']:

            aux = i['metrics']['market_data']

            assets[i['symbol']]=aux

        return assets


    def getMetrics(self, version):

        path = version + "/assets"

        response = self.__sendRequest(path).json()

        index = response['data'][0]

        layer1 = index.items()

        for key in layer1:

            print(key[0])

            print("\n")

            if key[0] =='metrics':

                for subKey in  key[1]:

                    print("\n"+ "----> " + subKey)

                    if key[1][subKey] == None:

                        print("\n"+ "     ----> " + "Empty")

                        print("\n")

                        continue

                    for subSubKey in key[1][subKey]:

                        print("\n" + "         ---->" + subSubKey)



    #### Date Format YY-mm-dd

    def getAssetsByTime(self, version,  asset, wich_metric, indicator, startDate, endDate, interval ):

        dt = datetime(2015, 10, 19,0,0,3,332).strftime('%Y-%m-%dT%H:%M:%S.%f')[0:-3]+'Z'

        print(dt)
        
        path = version + "/assets/" + asset + "/" + wich_metric + "/" + indicator + "/time-series" +"?start=" + "2022-08-30" + "&end=" + "2022-08-31" + "&interval="+ interval

        response = self.__sendRequest(path).json()

        return response

 

messari = Messari(API_KEY)


assetsData = messari.getAssetsData("v2",20 )

assets = messari.getAssets("v2",20)

marketcap = messari.getMarketCap("v2", 20)

marketData = messari.getMarketData("v2", 20)

assetByTime = messari.getAssetsByTime('v1', 'bitcoin','metrics', 'price', startDate, endDate, '1d' )


#print(assetsData)

#print(messari.getAssetsByTime("v1"))






#print(messari.getMarketData('v2', 20))






from asyncio.windows_events import NULL

import urllib
import datetime
from datetime import timezone, datetime
import requests
import json
import pandas as pd
import matplotlib.pyplot as plot

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

            assets[i['slug']] = i

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

    def getAssetsByTime(self, version,  asset, wich_metric, indicator, startDate, endDate, interval):

        startDay = datetime.strptime(startDate, "%Y-%m-%d").day

        startMonth = datetime.strptime(startDate, "%Y-%m-%d").month

        startYear = datetime.strptime(startDate, "%Y-%m-%d").year


        endDay = datetime.strptime(endDate, "%Y-%m-%d").day

        endMonth = datetime.strptime(endDate, "%Y-%m-%d").month

        endYear = datetime.strptime(endDate, "%Y-%m-%d").year

        ##### preencher ocm 21 horas no primeiro zero

        startDt = datetime(startYear, startMonth, startDay ,0,0,0,0).strftime('%Y-%m-%dT%H:%M:%S.%f')[0:-3]+'Z'

        endDt = datetime(endYear, endMonth, endDay ,0,0,0,0).strftime('%Y-%m-%dT%H:%M:%S.%f')[0:-3]+'Z'

        
        path = version + "/assets/" + asset + "/" + wich_metric + "/" + indicator + "/time-series" +"?start=" + startDt + "&end=" + endDt + "&interval="+ interval

        response = self.__sendRequest(path).json()

        return response

 

    def marketCap(self, version, limit):

        marketCapData = self.getMarketCap(version,limit)

        result = {}

        for i in marketCapData:

            result[i] = marketCapData[i]['current_marketcap_usd']

        return result




def priceChgWeek(limit, startDate, endDate):

    assets = messari.getAssets("v2",limit)


    result = {}

    for i in assets:

        assetByTime = messari.getAssetsByTime('v1', i,'metrics', 'price', startDate, endDate, '1d' )


        if assetByTime['data'] == None:

            result[i] = "No Data"

        else:

            result[i] = 100*(assetByTime['data']['values'][len(assetByTime['data']['values'])-1][4] - assetByTime['data']['values'][0][1])/assetByTime['data']['values'][0][1]

    return result
    

###### Essa função mostra a viração percentual de 0 hora de hoje até 0 hora do primeiro dia do mês

def chgMonthToDate(limit):

    today = datetime.today()

    firstDay = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')

    today = datetime.today().strftime('%Y-%m-%d')

    response = priceChgWeek(limit, firstDay, today)

    print(" Data range: " + 'From: ' + firstDay + " To " + today)

    return response






messari = Messari(API_KEY)


mktCapData=messari.marketCap('v2', 10)

mktCapData_dt = {'Cripto': mktCapData.keys(), 'Market Cap': mktCapData.values()}

mktCap = pd.DataFrame(mktCapData_dt)


mktCap.plot.bar(x='Cripto', y='Market Cap', title="Market Capitalization")

plot.show(block=True)


chgMonthToDateData=chgMonthToDate(10)

chgMonthToDateData_dt = {'Cripto': chgMonthToDateData.keys(), 'chgMontToDate': chgMonthToDateData.values()}

chgMTD = pd.DataFrame(chgMonthToDateData_dt)

chgMTD.plot.barh(x='Cripto', y='chgMontToDate', title="Change Month To Date")

plot.show(block=True)








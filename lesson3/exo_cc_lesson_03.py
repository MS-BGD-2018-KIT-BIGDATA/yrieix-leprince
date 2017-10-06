import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import json
from functools import reduce
from time import time
import pandas as pd

mykey = "AIzaSyC_NK7yLMdOc-kb9xWuTKgV0B2Td3dPyIM"


root = ['https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=', '&destinations=', '&key=']


def getDist(origin, dest):
    url = root[0] + origin + root[1] + dest + root[2] + mykey
    jsonData = json.loads(requests.get(url).text)
    try:
        gotdata = jsonData['rows'][0]["elements"][0]
    except IndexError:
        return -1
    if ('distance' in jsonData['rows'][0]["elements"][0]):
        return jsonData['rows'][0]["elements"][0]["distance"]["value"]
    else:
        return -1


df = pd.read_csv('villes_france.csv', sep=",")['ozan']


ori_cities = list(df)
dest_cities = sorted(list(df), reverse=True)
for ori, dest in zip(ori_cities, dest_cities):
    if ori != dest:
        dist = getDist(ori, dest)
        print(ori, dest, dist)
        if (dist != -1):
            trajet = {'origine':ori, 'destination':dest, 'distance': dist}

            df2 = pd.DataFrame()
            df2 = df2.append(trajet, ignore_index=True)



#print (json.dumps(jsonData, sort_keys=True,indent=4, separators=(',', ': ')))

import requests
import json
from bs4 import BeautifulSoup
from flaskApp.models import StatisticData, LatestTime
from flaskApp.extensions import db
from datetime import datetime
import time

    
def toDateTime(ticks):
    return datetime.fromtimestamp(ticks/1000)

def convertCities(dataList, countryName, provinceName, updateTime):
    result = []
    for item in dataList:
        data = StatisticData(countryName = countryName, provinceName = provinceName, updateTime=updateTime)
        data.cityName = item['cityName']
        data.confirmedCount = item['confirmedCount']
        data.suspectedCount = item['suspectedCount']
        data.curedCount = item['curedCount']
        data.deadCount = item['deadCount']
        result.append(data)
    return result

def convertProvinceList(dataList):
    result = []
    for item in dataList:
        data = StatisticData()
        data.countryName = item['country']
        data.provinceName = item['provinceName']
        data.updateTime = toDateTime(item['updateTime'])
        data.confirmedCount = item['confirmedCount']
        data.suspectedCount = item['suspectedCount']
        data.curedCount = item['curedCount']
        data.deadCount = item['deadCount']
        result.append(data)
        if 'cities' not in item:
            continue
        result.extend(convertCities(item['cities'], data.countryName, data.provinceName, data.updateTime))
    return result


def readProvinceDataFromIsaaclin():
    print('开始抓取疫情数据')
    try:
        url = 'https://lab.isaaclin.cn/nCoV/api/area?latest=0'
        r = requests.get(url, timeout=10)
        dataList = r.json()['results']
        return convertProvinceList(dataList)

    except Exception as e:
        print('readnProvinceDataFromIsaaclin error',str(e))
        return []




def convertOverallDataList(dataList):
    result = []
    for item in dataList:
        data = StatisticData()
        data.countryName = '全球'
        data.updateTime = toDateTime(item['updateTime'])
        data.confirmedCount = item['confirmedCount']
        data.suspectedCount = item['suspectedCount']
        data.curedCount = item['curedCount']
        data.deadCount = item['deadCount']
        result.append(data)
    return result

def readOverallDataFromIsaaclin():
    print('开始抓取全局疫情数据')
    try:
        url = 'https://lab.isaaclin.cn/nCoV/api/overall?latest=0'
        r = requests.get(url, timeout=10)
        dataList = r.json()['results']
        return convertOverallDataList(dataList)

    except Exception as e:
        print('readnOverallDataFromIsaaclin error',str(e))
        return []
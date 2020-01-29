import requests
import json
from bs4 import BeautifulSoup
from flaskApp.models import StatisticData
from datetime import datetime
import time


def toDateTime(ticks):
    return datetime.fromtimestamp(ticks/1000)


def convertTotalData(data):
    staticsData = StatisticData(countryName="全球")
    staticsData.updateTime = toDateTime(data['modifyTime'])
    staticsData.confirmedCount = data['confirmedCount']
    staticsData.suspectedCount = data['suspectedCount']
    staticsData.curedCount = data['curedCount']
    staticsData.deadCount = data['deadCount']
    return staticsData


def convertCities(dataList, provinceName, updateTime):
    result = []
    for item in dataList:
        data = StatisticData(countryName = "中国", updateTime=updateTime)
        data.provinceName = provinceName
        data.cityName = item['cityName']
        data.confirmedCount = item['confirmed']
        data.suspectedCount = item['suspected']
        data.curedCount = item['cured']
        data.deadCount = item['dead']
        result.append(data)
    return result

def convertProvinceList(dataList, updateTime):
    result = []
    for item in dataList:
        data = StatisticData(countryName = "中国", updateTime=updateTime)
        data.provinceName = item['provinceName']
        data.confirmedCount = item['confirmed']
        data.suspectedCount = item['suspected']
        data.curedCount = item['cured']
        data.deadCount = item['dead']
        result.append(data)
        cities = item['cities']
        if cities and len(cities) > 0:
            result.extend(convertCities(cities, item['provinceName'], updateTime))
    return result

def readnCoV():
    print('开始抓取疫情数据')
    try:
        url = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
        # url = 'http://lab.isaaclin.cn/nCoV/api/area?latest=0'
        r = requests.get(url, timeout=10)
        data = r.json()['data']
        totalData = convertTotalData(data['statistics'])
        result = [totalData]
        dataList = convertProvinceList(data['listByArea'], totalData.updateTime)
        result.extend(dataList)
        return result

    except Exception as e:
        print(str(e))
        return []

# readnCoV()
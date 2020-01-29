import requests
import json
from bs4 import BeautifulSoup
from flaskApp.models import StatisticData, LatestTime
from flaskApp.extensions import db
from datetime import datetime
import time


def getLastestUpdateTime():
    times = LatestTime.query.all()
    if not time != 1: 
        return datetime(2020, 1, 1, 0, 0, 0)
    return times[0].updateTime
    
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

def convertOtherCountryList(dataList, updateTime):
    result = []
    for item in dataList:
        data = StatisticData(updateTime=updateTime)
        data.countryName = item['name']
        data.confirmedCount = item['confirmed']
        data.suspectedCount = item['suspected']
        data.curedCount = item['cured']
        data.deadCount = item['dead']
        result.append(data)
    return result

def readnCoVFromTencent():
    print('开始抓取疫情数据')
    result = {'data':[], 'updateTime': datetime(2020,1,1)}
    try:
        lastTime = getLastestUpdateTime()
        url = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
        # url = 'http://lab.isaaclin.cn/nCoV/api/area?latest=0'
        r = requests.get(url, timeout=10)
        data = r.json()['data']
        totalData = convertTotalData(data['statistics'])
        if totalData.updateTime <= lastTime:
            print('数据未更新', totalData.updateTime)
            return result

        dataList = [totalData]

        dataList.extend(convertProvinceList(data['listByArea'], totalData.updateTime))
        dataList.extend(convertOtherCountryList(data['listByOther'], totalData.updateTime))
        return {
            'data': dataList,
            'updateTime': totalData.updateTime
        }

    except Exception as e:
        print('readnCoVFromTencent error',str(e))
        return result
import requests
import json
from bs4 import BeautifulSoup
from flaskApp.models import StatisticData, LatestTime, Area
from flaskApp.extensions import db
from flaskApp.utils import logger
from datetime import datetime
import time


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
    logger.info('开始抓取疫情数据')
    result = {'data':[], 'updateTime': datetime(2020,1,1)}
    try:
        lastTime = getLastestUpdateTime()
        url = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
        r = requests.get(url, timeout=10)
        data = r.json()['data']
        convertProvinceList(data['listByArea'], totalData.updateTime)
        convertOtherCountryList(data['listByOther'], totalData.updateTime)
        return {
            'data': dataList,
            'updateTime': totalData.updateTime
        }

    except Exception as e:
        logger.error('readnCoVFromTencent error, ' +str(e))
        return result
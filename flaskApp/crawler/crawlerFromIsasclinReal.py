import requests
import json
from bs4 import BeautifulSoup
from flaskApp.models import DataLogs, LatestTime
from flaskApp.extensions import db
from flaskApp.utils import logger
from datetime import datetime
import time

    
def getLastestUpdateTime():
    times = LatestTime.query.all()
    if not time != 1: 
        return datetime(2020, 1, 1, 0, 0, 0)
    return times[0].updateTime

def toDateTime(ticks):
    return datetime.fromtimestamp(ticks/1000)

def convertCities(dataList, countryName, provinceName, updateTime):
    result = []
    for item in dataList:
        try:
            data = DataLogs(countryName = countryName, provinceName = provinceName, updateTime=updateTime)
            data.cityName = item['cityName']
            data.confirmedCount = item['confirmedCount']
            data.suspectedCount = item['suspectedCount']
            data.curedCount = item['curedCount']
            data.deadCount = item['deadCount']
            result.append(data)
        except Exception as e:
            logger.warn('convert city error,' + item['cityName'])
    return result

def convertProvinceList(dataList, updateTime):
    result = []
    for item in dataList:
        try:
            data = DataLogs()
            data.countryName = item['countryName']
            data.provinceName = item['provinceName']
            data.updateTime = updateTime
            data.confirmedCount = item['confirmedCount']
            data.suspectedCount = item['suspectedCount']
            data.curedCount = item['curedCount']
            data.deadCount = item['deadCount']
            result.append(data)
            if 'cities' not in item or not item["cities"]:
                continue
            result.extend(convertCities(item['cities'], data.countryName, data.provinceName, data.updateTime))
        except Exception as e:
            logger.warn('convert province error,' +str(e) + item['provinceName'])
    return result


def readProvinceDataFromIsaaclin(updateTime):
    logger.info('抓取各省疫情数据')
    r = None
    txt = None
    try:
        url = 'https://lab.isaaclin.cn/nCoV/api/area?latest=1'
        r = requests.get(url, timeout=10)
        dataList = r.json()['results']
        return convertProvinceList(dataList, updateTime)

    except Exception as e:
        logger.error('readnProvinceDataFromIsaaclin error,' + str(e))
        logger.error(r.json())
        return []


def convertOverallDataList(item):
    data = DataLogs()
    data.countryName = '全球'
    data.updateTime = toDateTime(item['updateTime'])
    data.confirmedCount = item['confirmedCount']
    data.suspectedCount = item['suspectedCount']
    data.curedCount = item['curedCount']
    data.deadCount = item['deadCount']
    return data

def readOverallDataFromIsaaclin():
    logger.info('抓取全局疫情数据')
    try:
        url = 'https://lab.isaaclin.cn/nCoV/api/overall?latest=1'
        r = requests.get(url, timeout=10)
        dataList = r.json()['results']
        return convertOverallDataList(dataList[0])
    except Exception as e:
        logger.error('readnOverallDataFromIsaaclin error,' + str(e))
        return []

def readnCovFromIsasclin():
    logger.info('开始抓取疫情数据')
    result = {'data':[], 'updateTime': datetime(2020,1,1)}
    try:
        lastTime = getLastestUpdateTime()
        totalData = readOverallDataFromIsaaclin()
        if totalData.updateTime <= lastTime:
            logger.warning('数据未更新, ' + str(totalData.updateTime))
            return result
        dataList = [totalData]
        time.sleep(1)   
        dataList.extend(readProvinceDataFromIsaaclin(totalData.updateTime))
        return {
            'data': dataList,
            'updateTime': totalData.updateTime
        }

    except Exception as e:
        logger.error('readnCoVFromTencent error, ' +str(e))
        return result
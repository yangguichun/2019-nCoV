import requests
import json
from flaskApp.models import Area
from flaskApp.extensions import db
from flaskApp.utils import logger
from datetime import datetime
import time

def convertCities(dataList, parentName):
    result = []
    for item in dataList:
        data = Area(parentName=parentName, level="city")
        data.name = item['cityName']
        result.append(data)
    return result

def convertProvinceList(dataList):
    result = []
    for item in dataList:
        data = Area(parentName = "中国", level="province")
        data.name = item['provinceName']
        result.append(data)
        cities = item['cities']
        if cities and len(cities) > 0:
            result.extend(convertCities(cities, item['provinceName']))
    return result

def convertOtherCountryList(dataList):
    result = []
    for item in dataList:
        data = Area(parentName="全球", level="country")
        data.name = item['name']
        result.append(data)
    return result

def readnAreaFromTencent():
    logger.info('开始抓取区域数据')
    try:
        url = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
        r = requests.get(url, timeout=10)
        data = r.json()['data']
        dataList = []
        dataList.extend(convertProvinceList(data['listByArea']))
        dataList.extend(convertOtherCountryList(data['listByOther']))
        return dataList

    except Exception as e:
        logger.error('readnAreaFromTencent error, ' +str(e))
        return []
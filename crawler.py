import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


def readnCoV():
    print('开始抓所有历史数据')
    try:
        # stationCode = 'openId=odea75qpq7tzR9dBrz8-4Zb2FMw0,150,wxd2686a01b64dd27d,ltynw,13266839793,011CJ2o41pklhT1uZto41m6eo41CJ2ok,12,11.9%E5%85%AC%E9%87%8C,%E6%B7%B1%E5%9C%B3%E5%B8%82%E5%8D%97%E6%B9%BE%E8%A1%97%E9%81%93%E4%B8%B9%E7%AB%B9%E5%A4%B4%E7%A4%BE%E5%8C%BA%E9%BB%84%E7%AB%B9%E6%B5%AA%E4%B8%80%E5%8F%B7,%E9%99%86%E7%89%B9%E6%98%93%E5%8D%97%E6%B9%BE%E5%85%85%E7%94%B5%E7%AB%99,46726'
        url = 'https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia'
        # url = 'http://lab.isaaclin.cn/nCoV/api/area?latest=0'
        r = requests.get(url, timeout=10)
        print(r.text)

    except Exception as e:
        print(str(e))
        return None

readnCoV()
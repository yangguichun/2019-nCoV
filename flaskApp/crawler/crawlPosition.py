import requests
import json
from flaskApp.models import Area
from flaskApp.extensions import db
from flaskApp.utils import logger
from datetime import datetime
import time

def readPositionFromBaidu(name, parent):
    logger.info('读取%s %s经纬度',parent, name)
    try:
        url = f'http://api.map.baidu.com/geocoding/v3/?address={name}&city={parent}&output=json&ak=<your key>'
        # logger.info(url)
        r = requests.get(url, timeout=10)
        # logger.info('result %s', r.text)
        data = r.json()
        if data["status"] != 0:
          logger.error('读取%s %s经纬度信息失败, %s', parent, name, data)
          return None
        data = data['result']
        if data["level"] not in ["国家", "省份", "城市", "区县"]:
          logger.error('读取%s经纬度信息失败，返回数据级别不对, level=%s', name, data["level"])
          return None
        return data["location"]

    except Exception as e:
        logger.error('readPositionFromBaidu error, %s, %s,', name, str(e))
        return None
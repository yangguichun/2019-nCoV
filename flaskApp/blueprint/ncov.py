from flaskApp.models import StatisticData, Area
from flask import jsonify, request, render_template, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import and_, text
from datetime import datetime, timedelta
from flaskApp.utils import logger, strToDatetime

ncov_bp = Blueprint('ncov', __name__)


@ncov_bp.route('/index')
@ncov_bp.route('/')
def index():
    return render_template('index.html')


def convertCity(data):
    return {
        "name": data.cityName,
        "confirmedCount": data.confirmedCount,
        "suspectedCount": data.suspectedCount,
        "curedCount": data.curedCount,
        "deadCount": data.deadCount
    }

def convertProvince(data):
    return {
        "name": data.provinceName,
        "confirmedCount": data.confirmedCount,
        "suspectedCount": data.suspectedCount,
        "curedCount": data.curedCount,
        "deadCount": data.deadCount
    }

def getPositionList(nameList):
    nameStr =  ','.join(nameList)
    sql = f'name in ( {nameStr} )' 
    areaList = Area.query.filter(text(sql)).all()
    res = {}
    for area in areaList:
        res[area.name] = area
    return res

@ncov_bp.route('/allareadata/<level>/<date>', methods=['GET'])
def allAreaData(level, date):
    logger.info('allAreaData %s %s', level, date)
    startDate = date
    if strToDatetime(date) > datetime.now():
        return jsonify(code = -1, msg = "not supported error.")

    endDate = (strToDatetime(date) + timedelta(1)).strftime('%Y-%m-%d')
    dataList = StatisticData.query.distinct(StatisticData.countryName,StatisticData.provinceName, StatisticData.cityName).filter(and_(StatisticData.updateTime>startDate, StatisticData.updateTime<endDate)).order_by(StatisticData.countryName,StatisticData.provinceName, StatisticData.cityName, StatisticData.updateTime.desc()).all()
    if level == 'city':
        dataList = [convertCity(item) for item in dataList if item.cityName]
    elif level == 'province':
        dataList = [convertProvince(item) for item in dataList if (item.provinceName and not item.cityName) ]
    else:
        return jsonify(code = -1, msg = "not supported error.")
    posList = getPositionList([ '\''+item["name"]+'\'' for item in dataList])
    result = []
    for data in dataList:
        if data["name"] not in posList:
            continue
        data["lng"] = posList[data["name"]].longitude
        data["lat"] = posList[data["name"]].latitude
        result.append(data)        
    return jsonify(code=0, data=result)


@ncov_bp.route('/ncovtrend/<level>/<name>', methods=['GET'])
def ncovTrend(level, name):
    logger.info('level=%s, name=%s', level, name)
    dataList = []
    if level == 'country':
        dataList = StatisticData.query.filter(and_(StatisticData.countryName == name)).order_by(StatisticData.updateTime).all()
    elif level == 'province':
        dataList = StatisticData.query.filter(and_(StatisticData.provinceName == name)).order_by(StatisticData.updateTime).all()
    elif level == 'city':
        dataList = StatisticData.query.filter(and_(StatisticData.cityName == name)).order_by(StatisticData.updateTime).all()
    else:
        return jsonify(code=-1, msg="unsupported level")
    
    result = []
    for item in dataList:
        result.append({
            "updateTime": item.updateTime.strftime("%Y-%m-%d %H:%M"),
            "confirmedCount": item.confirmedCount,
            "suspectedCount": item.suspectedCount,
            "curedCount": item.curedCount,
            "deadCount": item.deadCount
        })
    return jsonify(code=0, data=result)
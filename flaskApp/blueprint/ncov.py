from flaskApp.models import DataLogs, Area, DayCaches
from flask import jsonify, request, render_template, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import and_, text, null
from datetime import datetime, timedelta
from flaskApp.utils import logger, strToDatetime

ncov_bp = Blueprint('ncov', __name__)


@ncov_bp.route('/index')
@ncov_bp.route('/')
def index():
    return render_template('index.html')



def getPositionList(nameList):
    nameStr =  ','.join(nameList)
    sql = f'name in ( {nameStr} )' 
    areaList = Area.query.filter(text(sql)).all()
    res = {}
    for area in areaList:
        res[area.name] = area
    return res


@ncov_bp.route('/arealist/<level>', methods=['GET'])
def areaList(level):
    # level, 只支持province, city
    if level not in ['city', 'province']:
        return jsonify(code=-1, msg="not supported level")

    def convertCity(areaList):
        resultDict = {}
        resultList = []
        for area in areaList:
            if area.parentName not in resultDict:
                resultList.append({
                    "text": area.parentName,
                    "children": []
                })
                resultDict[area.parentName] = []
            resultDict[area.parentName].append({ "text": area.name})
        # result = [ {"text": resultDict[item["text"]]} for item in resultList]
        for item in resultList:
            item["children"] = resultDict[item["text"]]
        return resultList

    def convertProvince(areaList):
        result = []
        for area in areaList:
            result.append({ "text": area.name})
        return result
            
    areaList = Area.query.filter(Area.level==level).all()
    result = None
    if level == 'city':
        result = convertCity(areaList)
    else:
        result = convertProvince(areaList)
    return jsonify(code = 0, data=result)
    
@ncov_bp.route('/allareadata/<level>/<date>', methods=['GET'])
def allAreaData(level, date):
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
    logger.info('allAreaData %s %s', level, date)
    startDate = date
    if strToDatetime(date) > datetime.now():
        return jsonify(code = -1, msg = "not supported error.")

    endDate = (strToDatetime(date) + timedelta(1)).strftime('%Y-%m-%d')
    dataList = DayCaches.query.filter(DayCaches.updateTime == date).all()
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


def getDatalogsQuery(level, name):
    if level == 'country':
        return DataLogs.query.filter(and_(DataLogs.countryName == name))
    elif level == 'province':
        return DataLogs.query.filter(and_(DataLogs.provinceName == name))
    elif level == 'city':
        return DataLogs.query.filter(and_(DataLogs.cityName == name))
    else: 
        return None

def dataLogToDict(datalog):
    if datalog:
        return {
            "updateTime": datalog.updateTime.strftime("%Y-%m-%d %H:%M"),
            "confirmedCount": datalog.confirmedCount,
            "suspectedCount": datalog.suspectedCount,
            "curedCount": datalog.curedCount,
            "deadCount": datalog.deadCount
        }
    else:
        return {
            "updateTime": datetime().strftime("%Y-%m-%d %H:%M"),
            "confirmedCount": 0,
            "suspectedCount": 0,
            "curedCount": 0,
            "deadCount":0         
        }
    
@ncov_bp.route('/datalogs/<level>/<name>', methods=['GET'])
def datalogs(level, name):
    logger.info('level=%s, name=%s', level, name)
    dataList = []
    query = getDatalogsQuery(level, name)
    if not query:
        return jsonify(code=-1, msg="param error")
    dataList = query.order_by(DataLogs.updateTime).all()    
    result = [dataLogToDict(item) for item in dataList]
    return jsonify(code=0, data=result)

@ncov_bp.route('/realtime/<level>/<name>', methods=['GET'])
def realtime(level, name):
    logger.info('level=%s, name=%s', level, name)
    dataList = []
    query = getDatalogsQuery(level, name)
    if not query:
        return jsonify(code=-1, msg="param error")
    datalog = query.order_by(DataLogs.updateTime.desc()).first()
    return jsonify(code=0, data= dataLogToDict(datalog))

# 获取每日增量数据
@ncov_bp.route('/incrementlogs/<level>/<name>', methods=['GET'])
def incrementlogs(level, name):
    logger.info('level=%s, name=%s', level, name)
    if level not in ['country', 'province', 'city']:
        return jsonify(code = -1, msg="not supported level")
    dayCountList = queryDayLogs(level, name)
    
    dayIncList = []
    for index, data in enumerate(dayCountList):
        item = data.copy()
        if index == 0:
            dayIncList.append(item)
            continue
        item["confirmedCount"] = data['confirmedCount'] - dayCountList[index-1]['confirmedCount']
        item["suspectedCount"] = data['suspectedCount'] - dayCountList[index-1]['suspectedCount']
        item["curedCount"] = data['curedCount'] - dayCountList[index-1]['curedCount']
        item["deadCount"] = data['deadCount'] - dayCountList[index-1]['deadCount']
        dayIncList.append(item)

    return jsonify(code=0, data=dayIncList)

def queryDayLogs(level, name):
    dataList = []
    if level == 'country':
        dataList = DayCaches.query.filter(and_(DayCaches.countryName == name)).order_by(DayCaches.updateTime).all()
    elif level == 'province':
        dataList = DayCaches.query.filter(and_(DayCaches.provinceName == name, DayCaches.cityName == None)).order_by(DayCaches.updateTime).all()
    elif level == 'city':
        dataList = DayCaches.query.filter(and_(DayCaches.cityName == name)).order_by(DayCaches.updateTime).all()
    else:
        return []

    dayCountList = []
    for item in dataList:
        dayCountList.append({
            "updateTime": item.updateTime.strftime("%Y-%m-%d"),
            "confirmedCount": item.confirmedCount,
            "suspectedCount": item.suspectedCount,
            "curedCount": item.curedCount,
            "deadCount": item.deadCount
        })
    return dayCountList

# 获取某个区域的每日数据列表
@ncov_bp.route('/daylogs/<level>/<name>', methods=['GET'])
def daylogs(level, name):
    logger.info('level=%s, name=%s', level, name)
    if level not in ['country', 'province', 'city']:
        return jsonify(code = -1, msg="not supported level")
    dataList = queryDayLogs(level, name)
    return jsonify(code=0, data=dataList)
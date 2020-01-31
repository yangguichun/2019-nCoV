from flaskApp.models import StatisticData
from chargeStationStatus.business.equalhours import EqualHourCalculator
from flask import jsonify, request, render_template, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import and_
import datetime
import chargeStationStatus.utils as utils

station_bp = Blueprint('station', __name__)


@station_bp.route('/index')
@station_bp.route('/')
def index():
    return render_template('index.html')


@station_bp.route('/calcstationincome/<id>', methods=['GET', 'POST'])
def calcStationIncome(id):
    data = request.get_json()
    stationId = id
    beginTime = '2019-4-15'
    endTime = '2019-4-16'
    serviceRate = 0.45
    # stationId = data["id"]
    # beginTime = data['beginTime']
    # endTime = data['endTime']
    # serviceRate = data['servieRate']

    # serviceRatePerPoint = serviceRate/12.0
    statusList = GunStatus.query.filter(and_(
        GunStatus.stationId == stationId, GunStatus.queryTime > beginTime, GunStatus.queryTime < endTime)).all()
    totalIncome = 0.0
    totalKwh = 0.0
    for item in statusList:
        if item.status == 1:
            # 除以12是因为每个测点的间隔是5分钟
            totalIncome = totalIncome + item.power/12.0

    return jsonify(code=0, totalKwh=totalKwh, income=totalIncome*serviceRate)


@station_bp.route('/getstationlist')
@login_required
def getStaionList():
    stationList = ChargeStation.query.all()
    result = []
    for station in stationList:
        oneStation = {}
        oneStation["id"] = station.id
        oneStation["name"] = station.stationName
        result.append(oneStation)
    return jsonify(stationList=result)


def toArray(aDict):
    aList = list(
        map(lambda item: {'id': None, 'name': item}, list(aDict.keys())))
    for item in aList:
        item['children'] = aDict[item['name']]
    return aList


@station_bp.route('/getstationtree')
@login_required
def getStaionTree():
    stationList = []
    # 超级管理员就读取所有，其他人就要分配
    if current_user.name == 'admin':
        stationList = ChargeStation.query.all()
    else:
        stationList = current_user.stations

    result = {}
    for station in stationList:
        if not station.enable:
            continue

        oneStation = {}
        oneStation["id"] = station.id
        oneStation["name"] = '{}({})'.format(
            station.gunTotalCount, station.stationName)
        if not (station.region in result):
            result[station.region] = []
        result[station.region].append(oneStation)

    return jsonify(stationList=toArray(result))


@station_bp.route('/stationstatus/<ids>')
@login_required
def getStatus(ids):
    idList = ids.split('_')
    result = {}
    stationList = ChargeStation.query.filter(
        ChargeStation.id.in_(idList)).all()
    for station in stationList:
        result[station.id] = {"name": station.stationName, "value": []}

    statusList = ChargeStationStatus.query.filter(and_(ChargeStationStatus.stationId.in_(
        idList), ChargeStationStatus.queryTime > '2019-4-13 22:00:00')).order_by(ChargeStationStatus.queryTime).all()
    for item in statusList:
        percent = round(item.usedGunCount /
                        (item.usedGunCount + item.freeGunCount), 2)
        oneStatus = [item.queryTime.strftime("%Y-%m-%d %H:%M"), percent]
        result[item.stationId]["value"].append(oneStatus)

    return jsonify(stationList=result)


def toDateTimeSpans(timeSpans):
    result = []
    for span in timeSpans:
        newSpan = {}
        newSpan['beginTime'] = utils.isoformatToTime(span['beginTime'])
        newSpan['endTime'] = utils.isoformatToTime(span['endTime'])
        result.append(newSpan)
    return result


@station_bp.route('/station_equalhours', methods=['POST', 'GET'])
@login_required
def queryStationEqualHours():
    # 获取指定日期范围内的每一天的指定时间段的使用等效小时数
    result = {
        'header': {
            'code': 0,
            'msg': '成功'
        }
    }
    data = request.get_json()
    if data is None:
        result['header']['code'] = -1
        result['header']['msg'] = '入参格式错误'
        return jsonify(result=result)

    idList = data["ids"]
    # 起止日期
    # 查询的时候
    beginDate = utils.isoformatToDate(data['beginDate'])
    endDate = utils.isoformatToDate(data['endDate'])

    # 这个指统计的时候，要包含一天中哪个时间范围的数据
    timeSpans = toDateTimeSpans(data['timeSpans'])

    calc = EqualHourCalculator()
    result['data'] = calc.queryStationEqualHours(
        idList, beginDate, endDate, timeSpans)
    return jsonify(result)


@station_bp.route('/station_incomebytou', methods=['POST', 'GET'])
def queryStationIncomeByTou():
    data = request.get_json()
    print(data)
    return jsonify(result=data)
    if data is None:
        result = {
            "code": -1,
            "msg": '入参格式错误'
        }
        return jsonify(result=result)

    idList = data["ids"]
    # 起止日期
    # 查询的时候
    beginDate = utils.isoformatToDate(data['beginDate'])
    endDate = utils.isoformatToDate(data['endDate'])

    # 这个指统计的时候，要包含一天中哪个时间范围的数据
    timeSpans = toDateTimeSpans(data['timeSpans'])
    tou = data['tou']


@station_bp.route('/querystatus_percent', methods=['POST', 'GET'])
@login_required
def queryStationStatus_ByPercent():
    data = request.get_json()
    idList = data["ids"]

    beginTime = data['beginTime']
    endTime = data['endTime']
    print(data)

    result = {}
    stationList = ChargeStation.query.filter(
        ChargeStation.id.in_(idList)).all()
    for station in stationList:
        result[station.id] = {"name": station.stationName, "value": []}

    statusList = ChargeStationStatus.query.filter(and_(ChargeStationStatus.stationId.in_(
        idList), ChargeStationStatus.queryTime > beginTime, ChargeStationStatus.queryTime < endTime)).order_by(ChargeStationStatus.queryTime).all()
    for item in statusList:
        total = item.usedGunCount + item.freeGunCount + item.fixedGunCount
        percent = 0
        if total > 0:
            percent = round(item.usedGunCount/total, 2)
        oneStatus = [item.queryTime.strftime("%Y-%m-%d %H:%M"), percent]
        result[item.stationId]["value"].append(oneStatus)

    return jsonify(stationList=result)


@station_bp.route('/querystatus_num', methods=['POST', 'GET'])
@login_required
def queryStationStatus_ByNum():
    data = request.get_json()
    idList = data["ids"]

    beginTime = data['beginTime']
    endTime = data['endTime']
    print(data)

    result = {}
    stationList = ChargeStation.query.filter(
        ChargeStation.id.in_(idList)).all()
    for station in stationList:
        result[station.id] = {"name": station.stationName, "value": []}

    statusList = ChargeStationStatus.query.filter(and_(ChargeStationStatus.stationId.in_(
        idList), ChargeStationStatus.queryTime > beginTime, ChargeStationStatus.queryTime < endTime)).order_by(ChargeStationStatus.queryTime).all()
    for item in statusList:
        oneStatus = [item.queryTime.strftime(
            "%Y-%m-%d %H:%M"), item.usedGunCount]
        result[item.stationId]["value"].append(oneStatus)

    return jsonify(stationList=result)

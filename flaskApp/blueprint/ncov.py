from flaskApp.models import StatisticData
from flask import jsonify, request, render_template, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import and_
import datetime
from flaskApp.utils import logger


ncov_bp = Blueprint('ncov', __name__)


@ncov_bp.route('/index')
@ncov_bp.route('/')
def index():
    return render_template('index.html')


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
from flaskApp.extensions import db
from flaskApp.models import StatisticData
from flaskApp.crawler import readnCoV
import click
import schedule
from datetime import datetime
import time


def do_crawl():
    dataList = readnCoV()
    if dataList is None:
        return False

    try:
        click.echo('开始写入数据...')
        for item in dataList:
            db.session.add(item)
            db.session.commit()
        click.echo('写入数据完成...')

        return True
    except BaseException as e:
        print('抓取发生异常', str(e))
        return False

def register_commands(app):
    @app.cli.command()
    def crawl():
        try:
            do_crawl()
            schedule.every(15).seconds.do(do_crawl)
            while True:
                schedule.run_pending()
                time.sleep(1)
        except BaseException as e:
            print('主循环异常退出...', str(e))

    @app.cli.command()
    def test():
        a = [1, 2, 3]
        b = 1
        if b in a:
            print('in can work')

        c = 4
        if c not in a:
            print('not in can work')


    @app.cli.command()
    @click.argument('name')
    @click.argument('serial')
    @click.argument('count')
    def add(name, serial, count):
        station = ChargeStation(stationName = name, stationNo = serial, gunTotalCount = count)
        db.session.add(station)
        db.session.commit()
        click.echo('成功添加了充电站 ' + name)


    @app.cli.command()
    def read():
        stations = ChargeStation.query.all()
        for station in stations:
            click.echo(station.to_json())
        click.echo('读取电站成功')


    @app.cli.command()
    @click.argument('id')
    def delete(id):
        station = ChargeStation.query.filter_by(id=id).first()
        stationName = station.stationName
        db.session.delete(station)
        db.session.commit()
        click.echo('成功删除电站：' + stationName)
    
    
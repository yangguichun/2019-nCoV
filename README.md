### 概述
主要包括两个页面
- 趋势，默认显示整体的数据，包括总量的趋势，以及确诊、疑似、治愈、死亡的每日增量；
  - 可以选择查询某个省份或者某个城市的趋势数据
  - ![trend page](/doc/trend.png)
- 分布，显示肺炎的分布
  - 可以查询历史上每一天的数据
  - 可以选择显示省份还是城市的数据
  - 可以选择数据类型：确诊、治愈还是死亡
  - ![distribute page](/doc/distribute.jpg)

### 使用说明
- 数据库
  - 安装postgresql
  - 创建数据库，名字为 feiyan
  - 还原数据，在root账户下使用pg_restore导入数据，截止2020-02-20的数据，`feiyan-db-20200202.backup`文件位于 `/data`目录下，导入时换成具体的本地目录
```shell
pg_restore --host=127.0.0.1 --port=5432 --username="youpguser" --dbname="feiyan" --password  --list /home/feiyan-db-20200202.backup
```
- 爬虫与后端，
  - 创建python运行环境，本项目依赖python V3.6及其以上版本
  - 项目使用pipenv管理依赖，所以先安装pipenv
  ```shell
   pip install pipenv
   ```
  - 在项目目录下使用pipenv创建虚拟环境: pipenv install
  - 进入虚拟环境： pipenv shell
  - 运行爬虫: flask crawl，这样程序就会每15分钟检测一次数据是否有更新
  - 运行web服务
  ```shell
  flask run --host=0.0.0.0 --port=8080
  ```
  - 前端
    - 默认已经在template和static目录下编译好了最新的前端
    - 如果要修改和测试前端代码，可以直接npm run serve来测试，默认会使用 `http://47.107.190.155:8081`上的api，可以改为你本地的api，可以在`vue.config.js`中修改
    - 修改之后运行npm run build，会生成到template和static目录下


### 开发环境
- 数据库 postgresql
- 爬虫
  - python
  - requests
- 后端
  - python，以及如下组件
```
flask = "*"
flask-sqlalchemy = "*"
requests = "*"
flask-migrate = "*"
python-dotenv = "*"
psycopg2 = "*"
schedule = "*"
flask-login = "*"
```
- 前端
  - vue.js
  - vant
  - echarts
  - moment.js


### 参考资料
- 数据抓取，参考[这里](https://github.com/BlankerL/DXY-2019-nCoV-Crawler)
- 数据展示，参考[这里](https://blog.csdn.net/xufive/article/details/104093197)

### 资源
- [腾讯的读数实时肺炎数据接口](https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia)，[显示界面](https://news.qq.com/zt2020/page/feiyan.htm#charts)
- [某人抓取的从2020-1-24号之后总体的历史数据接口](https://lab.isaaclin.cn/nCoV/api/overall?latest=0)
- [某人抓取的从2020-1-24号之后各省份历史数据接口](https://lab.isaaclin.cn/nCoV/api/area?latest=0)，[说明文档](https://lab.isaaclin.cn/nCoV/)


### 其他
- [修改pip到国内源](https://www.cnblogs.com/schut/p/10410087.html)
- [pipenv官网](https://github.com/pypa/pipenv)
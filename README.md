### 概述
主要包括两个页面
- 趋势，默认显示整体的数据，包括总量的趋势，以及确诊、疑似、治愈、死亡的每日增量；
  - 可以选择查询某个省份或者某个城市的趋势数据
![trend page](/doc/trend.png)
- 分布，显示肺炎的分布
  - 可以查询历史上每一天的数据
  - 可以选择显示省份还是城市的数据
  - 可以选择数据类型：确诊、治愈还是死亡
![distribute page](/doc/distribute.jpg)

### 运行环境
- python
    - flask
    - flask-sqlalchemy
    - request
    - beautiful soap
- 数据库 postgresql

### 使用说明
- 安装好postgresql
  - 创建名字为 feiyan 的数据库
- 在项目目录下运行如下命令
```shell
pip install pipenv
pipenv install
pipenv shell
flask run

```

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
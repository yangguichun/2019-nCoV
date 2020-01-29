### 项目目标
- 抓取从2020-01-24之后的所有疫情数据，包括每个省，每个市的
- 每个小时抓取一次，把所有历史数据存储在数据库
- 提供api，可以让用户查询每个省市的历史数据
- 提供界面
  - 棒图、饼图，展示每个省市的各数据的时间维度的变化
  - 地图，展示各省市随着时间推移，疫情数据的变化在地图上用颜色标注

### 进度计划
- 1-29，完成数据抓取和存储
- 1-30，完成数据的chart展示


### 参考资料
- 数据抓取，参考[这里](https://github.com/BlankerL/DXY-2019-nCoV-Crawler)
- 数据展示，参考[这里](https://blog.csdn.net/xufive/article/details/104093197)

### 资源
- [腾讯的读数实时肺炎数据接口](https://service-f9fjwngp-1252021671.bj.apigw.tencentcs.com/release/pneumonia)，[显示界面](https://news.qq.com/zt2020/page/feiyan.htm#charts)
- [某人抓取的从2020-1-24号之后的历史数据接口](https://lab.isaaclin.cn/nCoV/api/area?latest=0)，[说明文档](https://lab.isaaclin.cn/nCoV/)


### 其他
- [修改pip到国内源](https://www.cnblogs.com/schut/p/10410087.html)
- [pipenv官网](https://github.com/pypa/pipenv)
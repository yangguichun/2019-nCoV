### 20200131
- TODO:
  - ~~添加表，记录省市列表，以及他们的经纬度~~
  - ~~接口：获取最新的所有省的数据~~
  - ~~接口：获取最新的所有市的数据~~
  - ~~接口：获取指定日期的省份数据，其实就是获取该日期的最后一条~~，对应的sql语句如下。
  >select distinct on("countryName", "provinceName", "cityName") "countryName", "provinceName", "cityName","updateTime", 
       "confirmedCount", "suspectedCount", "curedCount", "deadCount" from data_logs where "updateTime" > '2020-01-30' and "updateTime" <'2020-01-31' order by "countryName", "provinceName", "cityName", "updateTime" desc
  - ~~接口：获取指定日期的城市数据~~
  - 接口：获取每个省份、城市每天的增量数据
  - 接口：获取所有省份列表
  - 接口：获取所有省份，以及下面的城市树型结构

- bugfix: 
  - 使用vue-axios，然后在vue.config.js配置了代理，访问api时提示No 'Access-Control-Allow-Origin' header is present on the requested resource.，后来换成vue-resource就可以了，估计是axios要做什么配置。
- 参考资料：
  - [高德地图获取行政区域的接口](https://lbs.amap.com/api/webservice/guide/api/district/)
  - [百度地图获取经纬度接口](http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding)
  - [sqlalchemy 排序，倒序](https://segmentfault.com/q/1010000010543918), `Phone.query.filter_by(brand=brand).order_by(Phone.added.desc()).first()`
  - [sqlalchemy, order_by，多个字段](https://www.cnblogs.com/Purk/p/6018533.html)，`db.query(Parent).order_by(Parent.id,Parent.name).all()`
  - sqlalchemy的源码是一个不错的参考资料，对于不熟悉的api，只能去看源码，比如distinct()方法的用法
  - [sqlalchemy 如何使用原始sql](file:///E:/2.src/gitbase/sqlalchemy/doc/doc/core/tutorial.html#using-more-specific-text-with-table-literal-column-and-column)，可以用text方法

  ### 20200201
  - TODO:
    - 添加命令：历史每天的每个区域的最后一条数据转存到缓存表中
    - 添加表：缓存表，表结构和历史表一样，只是里面存储的是每天的最后一条数据，updateTime就是日期，每个区域每天一条数据
    - 修改爬虫：每次抓取到数据之后，将数据存储到历史表的同时，也存储一份到缓存表
    - 接口：获取每个省份、城市每天的增量数据
    - 接口：获取所有省份列表
    - 接口：获取所有省份，以及下面的城市树型结构
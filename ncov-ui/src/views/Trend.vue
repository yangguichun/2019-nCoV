<template>
  <div>
    <div class="title">2020肺炎分布</div>
    <div class="date-picker">
      <van-button type="primary" size="small" @click="onPrevious">前一天</van-button>
      <div class="date-val">{{theDateStr}}</div>
      <van-button type="primary" size="small" @click="onNext">后一天</van-button>
    </div>
    <div class="data-type">
      <van-tag round class="data-item" type="danger" @click="onConfirm">确诊</van-tag>
      <van-tag round class="data-item" type="primary" @click="onSuspect">疑似</van-tag>
      <van-tag round class="data-item" type="success" @click="onCured">治愈</van-tag>
      <van-tag round class="data-item" @click="onDead">死亡</van-tag>
    </div>
    <div class="area-type"></div>
    <v-chart :options="mapOption" class="map" />
    <v-chart :options="lineOption" class="line" />
  </div>
</template>
<script>
import moment from "moment";
import ECharts from "vue-echarts";
import chinaMap from "../map-data/china.json";
ECharts.registerMap("china", chinaMap);
import mapOption from "../chart-options/map";
import lineOption from "../chart-options/line";
import "echarts";

export default {
  components: {
    "v-chart": ECharts
  },
  data() {
    return {
      mapOption,
      lineOption,
      theDate: moment(),
      theDateStr: moment().format("YYYY-MM-DD"),
      minDate: moment("2020-01-24"),
      maxDate: moment(
        moment()
          .add(1, "d")
          .format("YYYY-MM-DD")
      ),
      dataName: 'confirmedCount',
      selectedData:{
        name: 'confirmedCount',
        color: '#ff0000'
      },
      level: 'city'
    };
  },
  computed: {},
  methods: {
    onPrevious() {
      console.log("onPrevious");
      this.theDate.add(-1, "d");
      if (this.theDate < this.minDate) {
        this.theDate.add(1, "d");
        return;
      }
      this.theDateStr = this.theDate.format("YYYY-MM-DD");
      this.queryTheDateData();
    },
    onNext() {
      console.log("onNext");
      this.theDate.add(1, "d");
      if (this.theDate > this.maxDate) {
        this.theDate.add(-1, "d");
        return;
      }
      this.theDateStr = this.theDate.format("YYYY-MM-DD");
      this.queryTheDateData();
    },
    onConfirm(){
      console.log('onConfirm')
      this.mapOption.title.text="确诊人数"
      // this.mapOption.series[0].itemStyle.color = 'rgb(255,127,39)'
      this.mapOption.series[0].itemStyle.color = 'rgb(255,12,39)'
      this.mapOption.series[0].symbolSize = (val) =>{
        let size = Math.min(val[2] / 15, 25)
        if (size < 2) size = 2
          return size;
      }
      this.dataName = 'confirmedCount'
      this.queryTheDateData();
    },
    onSuspect(){
      console.log('onSuspect')
      this.mapOption.title.text="疑似人数"
      this.mapOption.series[0].itemStyle.color = 'rgb(13,94,242)'
      this.mapOption.series[0].symbolSize = (val) =>{
        let size = Math.min(val[2] / 15, 25)
        if (size < 2) size = 2
          return size;
      }
      this.dataName = 'suspectedCount'
      this.queryTheDateData();
    },
    onCured(){
      console.log('onCured')
      this.mapOption.title.text="治愈人数"
      this.mapOption.series[0].itemStyle.color = 'rgb(0, 151, 15)'
      this.mapOption.series[0].symbolSize = (val) =>{
        let size = Math.min(val[2] / 3, 25)
        if (size < 2) size = 2
          return size;
      }
      this.dataName = 'curedCount'
      this.queryTheDateData();

    },
    onDead(){
      console.log('onDead')
      this.mapOption.title.text="死亡人数"
      this.mapOption.series[0].itemStyle.color = 'rgb(100, 100, 100)'
      this.mapOption.series[0].symbolSize = (val) =>{
        let size = Math.min(val[2] / 3, 25)
        if (size < 2) size = 2
          return size;
      }
      this.dataName = 'deadCount'
      this.queryTheDateData();
    },
    calcMax(dataList) {
      let max = dataList.reduce((prev, curr) => {
        console.log(
          "calcmax",
          prev,
          curr.confirmedCount,
          curr.suspectedCount,
          curr.curedCount,
          curr.deadCount
        );
        return Math.max(
          prev,
          curr.confirmedCount,
          curr.suspectedCount,
          curr.curedCount,
          curr.deadCount
        );
      }, 0);
      return max;
    },
    queryTheDateData() {
      return this.$http
        .get(`/allareadata/${this.level}/${this.theDateStr}`)
        .then(res => {
          console.log("queryTheDateData success", res.data);
          let data = res.data;
          if (data.code != 0) {
            console.log("queryTheDateData success", data.msg);
            return;
          }
          let dataList = res.data.data;
          let formatedList = dataList.map(item => {
            return {
              name: item.name,
              value: [item.lng, item.lat, item[this.dataName]]
            };
          });
          this.mapOption.series[0].data = formatedList;
        })
        .catch(res => {
          console.log("queryTheDateData fail", res.data);
        });
    },
    queryTrendData(level, area) {
      return this.$http
        .get(`/datalogs/${level}/${area}`)
        .then(response => {
          console.log("queryTrendData success", response.data);
          let data = response.data;
          if (data.code != 0) {
            console.log("queryTrendData success", data.msg);
            return;
          }
          let dataList = response.data.data;
          this.lineOption.series[0].data = dataList.map(data => {
            return {
              name: data.updateTime,
              value: [data.updateTime, data.confirmedCount]
            };
          });
          this.lineOption.series[1].data = dataList.map(data => {
            return {
              name: data.updateTime,
              value: [data.updateTime, data.suspectedCount]
            };
          });
          this.lineOption.series[2].data = dataList.map(data => {
            return {
              name: data.updateTime,
              value: [data.updateTime, data.curedCount]
            };
          });
          this.lineOption.series[3].data = dataList.map(data => {
            return {
              name: data.updateTime,
              value: [data.updateTime, data.deadCount]
            };
          });
          let max = this.calcMax(dataList);
          console.log("max value", max);
          this.lineOption.yAxis.max = parseInt(max * 1.1);
        })
        .catch(res => {
          console.log("queryTrendData failed", res);
        });
    }
  },
  mounted() {
    this.queryTrendData("country", "全球");
    // this.queryTheDateData('province', '2020-1-30')
    this.queryTheDateData();
  }
};
</script>
<style lang='scss' scoped>
.map {
  width: 750px;
  height: 500px;
}
.line {
  margin-top: 20px;
  width: 750px;
  height: 550px;
}
.title{
  font-size: 36px;
  font-weight: bold;
  padding: 20px 5px;
}
.date-picker {
  margin: 15px 5px;
  .date-val {
    display: inline-block;
    padding: 5px 10px;
  }
}
.data-type{
  margin: 15px 5px;
  .data-item{
    margin: 0 20px;
  }
}
</style>
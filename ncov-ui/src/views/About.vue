<template>
  <div>
    <van-button type="default">默认按钮</van-button>
    <v-chart :options="mapOption" class="map" />
    <v-chart :options="lineOption" class="line" />
  </div>
</template>
<script>
import moment from 'moment'
import ECharts from "vue-echarts";
import chinaMap from "../map-data/china.json";
ECharts.registerMap("china", chinaMap);
import mapOption from "../chart-options/map";
import "echarts";

export default {
  components: {
    "v-chart": ECharts
  },
  data() {
    return {
      mapOption,
      lineOption: {
        title: {
          text: "动态数据 + 时间坐标轴"
        },
        tooltip: {
          trigger: "axis",
          formatter: function(params) {
            params = params[0];
            var date = new Date(params.name);
            return (
              date.getDate() +
              "/" +
              (date.getMonth() + 1) +
              "/" +
              date.getFullYear() +
              " : " +
              params.value[1]
            );
          },
          axisPointer: {
            animation: false
          }
        },
        xAxis: {
          type: "time",
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: "value",
          boundaryGap: [0, "100%"],
          splitLine: {
            show: false
          }
        },
        series: [
          {
            name: "确诊",
            type: "line",
            showSymbol: false,
            hoverAnimation: false,
            data: []
          },
          {
            name: "疑似",
            type: "line",
            showSymbol: false,
            hoverAnimation: false,
            data: []
          }
        ]
      }
    };
  },
  computed: {},
  methods: {
    generateData(rate){
      let startTime = moment('2020-01-20')
      let endTime = moment('2020-01-31')
      let value = 0
      let datas = []
      while(startTime<endTime){
        startTime.add(1, 'h')
        value += parseInt(Math.random()*rate)
        datas.push({
          name: startTime.format('YYYY-MM-DD HH:mm'),
          value: [
            startTime.format('YYYY-MM-DD HH:mm'), value
          ]
        })
      }
      return datas
    }
  },
  mounted() {
    this.lineOption.series[0].data = this.generateData(10)
    this.lineOption.series[1].data = this.generateData(3)
  }
};
</script>
<style lang='scss' scoped>
.map {
  width: 750px;
  height: 450px;
}
.line {
  width: 750px;
  height: 550px;
}
</style>
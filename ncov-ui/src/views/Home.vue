<template>
  <div>
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
          text: "2019武汉肺炎数据"
        },
        tooltip: {
          trigger: "axis",
          formatter: function(params) {
            console.log('formatter,', params)
            // params = params[0];
            // let thetime = moment(params.name)
            // console.log('moment format', thetime.format('YYYY-MM-DD HH:mm'),)
            // return (
            //   thetime.format('YYYY-MM-DD HH:mm'),
            //   params.value[1]
            // );
            let time = `${params[0].name}<br>`
              let values = params.map( item =>{
                return `${item.seriesName}: ${item.value[1]}`
              })
              return time + values.join('<br>')
          },
          position: function (pos, params, el, elRect, size) {
                var obj = {top: 30};
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            }
        },
        legend: {
          icon: "rect",
          itemWidth: 10,
          itemHeight: 5,
          textStyle: {
            color: "rgba(104,104,104,1)",
            fontSize: 12
          },
          // left: 'auto',
          top: "15%"
        },
        grid: {
          show: true,
          left: "3%",
          right: "3%",
          bottom: "0%",
          top: "25%",
          containLabel: true,
          borderColor: "rgba(255,255,255,1)"
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
          // splitLine: {
          //   show: false
          // },
          min: 0,
          max: 20000
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
          },
          {
            name: "治愈",
            type: "line",
            showSymbol: false,
            hoverAnimation: false,
            data: []
          },
          {
            name: "死亡",
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
    generateData(rate) {
      let startTime = moment("2020-01-20");
      let endTime = moment("2020-01-31");
      let value = 0;
      let datas = [];
      while (startTime < endTime) {
        startTime.add(1, "h");
        value += parseInt(Math.random() * rate);
        datas.push({
          name: startTime.format("YYYY-MM-DD HH:mm"),
          value: [startTime.format("YYYY-MM-DD HH:mm"), value]
        });
      }
      return datas;
    },
    calcMax(dataList){
      let max = dataList.reduce((prev, curr) =>{
        console.log('calcmax', prev, curr.confirmedCount, curr.suspectedCount, curr.curedCount, curr.deadCount)
        return Math.max(prev, curr.confirmedCount, curr.suspectedCount, curr.curedCount, curr.deadCount)
      }, 0)
      return max;
    },
    queryData() {
      this.$http.get('/ncovtrend/country/全球')
        .then(response => {
          console.log('querydata success', response.data);
          let dataList = response.data.data
          this.lineOption.series[0].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.confirmedCount]}})
          this.lineOption.series[1].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.suspectedCount]}})
          this.lineOption.series[2].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.curedCount]}})
          this.lineOption.series[3].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.deadCount]}})
          let max = this.calcMax(dataList)
          console.log('max value', max)
          this.lineOption.yAxis.max = max*1.2
        })
        .catch( res =>{
          console.log('query data failed', res)
        })
    }
  },
  mounted() {
    this.queryData()
  }
};
</script>
<style lang='scss' scoped>
.map {
  width: 750px;
  height: 450px;
}
.line {
  margin-top: 20px;
  width: 750px;
  height: 550px;
}
</style>
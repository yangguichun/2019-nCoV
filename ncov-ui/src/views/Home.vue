<template>
  <div>
    <van-button type="default" @click="onPrevious">前一天</van-button>
    {{theDateStr}}
    <van-button type="default" @click="onNext">后一天</van-button>
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
      theDateStr:moment().format('YYYY-MM-DD'),
      minDate: moment("2020-01-24"),
      maxDate: moment(moment().add(1, 'd').format('YYYY-MM-DD')),
    };
  },
  computed: {},
  methods: {
    onPrevious(){
      console.log('onPrevious')
      this.theDate.add(-1, 'd')
      if(this.theDate < this.minDate){
        this.theDate.add(1, 'd')
        return
      } 
      this.theDateStr = this.theDate.format('YYYY-MM-DD')
      this.queryTheDateData('city', this.theDateStr)
    },
    onNext(){
      console.log('onNext')
      this.theDate.add(1, 'd')
      if(this.theDate > this.maxDate){
        this.theDate.add(-1, 'd')
        return 
      }
      this.theDateStr = this.theDate.format('YYYY-MM-DD')
      this.queryTheDateData('city', this.theDateStr)
    },
    calcMax(dataList){
      let max = dataList.reduce((prev, curr) =>{
        console.log('calcmax', prev, curr.confirmedCount, curr.suspectedCount, curr.curedCount, curr.deadCount)
        return Math.max(prev, curr.confirmedCount, curr.suspectedCount, curr.curedCount, curr.deadCount)
      }, 0)
      return max;
    },
    queryTheDateData(level, theDate){
      return this.$http.get(`/allareadata/${level}/${theDate}`)
        .then( res => {
          console.log('queryTheDateData success', res.data)
          let data = res.data
          if(data.code != 0){
            console.log('queryTheDateData success', data.msg)
            return
          }
          let dataList = res.data.data
          let confirmedList = dataList.map( item =>{
            return {
              name: item.name,
              value: [item.lng, item.lat, item.confirmedCount]
            }
          })
          this.mapOption.series[0].data = confirmedList
        })
        .catch( res =>{
          console.log('queryTheDateData fail', res.data)

        })
    },
    queryTrendData(level, area) {
      return this.$http.get(`/ncovtrend/${level}/${area}`)
        .then(response => {
          console.log('queryTrendData success', response.data);
          let data = response.data
          if(data.code != 0){
            console.log('queryTrendData success', data.msg)
            return
          }
          let dataList = response.data.data
          this.lineOption.series[0].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.confirmedCount]}})
          this.lineOption.series[1].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.suspectedCount]}})
          this.lineOption.series[2].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.curedCount]}})
          this.lineOption.series[3].data = dataList.map( data =>{ return {name: data.updateTime, value: [data.updateTime, data.deadCount]}})
          let max = this.calcMax(dataList)
          console.log('max value', max)
          this.lineOption.yAxis.max = parseInt(max*1.1)
        })
        .catch( res =>{
          console.log('queryTrendData failed', res)
        })
    }
  },
  mounted() {
    this.queryTrendData('country', '全球')
    // this.queryTheDateData('province', '2020-1-30')
    this.queryTheDateData('city', this.theDateStr)
  }
};
</script>
<style lang='scss' scoped>
.map {
  width: 750px;
  height: 550px;
}
.line {
  margin-top: 20px;
  width: 750px;
  height: 550px;
}
</style>
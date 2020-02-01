<template>
  <div>
    <div class="title">2020肺炎时间趋势</div>
    <!-- <div class="data-type">
      <van-tag round class="data-item" type="danger" @click="onConfirm">确诊</van-tag>
      <van-tag round class="data-item" type="primary" @click="onSuspect">疑似</van-tag>
      <van-tag round class="data-item" type="success" @click="onCured">治愈</van-tag>
      <van-tag round class="data-item" @click="onDead">死亡</van-tag>
    </div> -->
    <div class="area-type"></div>
    <v-chart :options="lineOption" class="line" />
    <v-chart :options="confirmedIncBarOption" class="stack-bar" />
    <v-chart :options="suspectedIncBarOption" class="stack-bar" />
    <v-chart :options="curedIncBarOption" class="stack-bar" />
    <v-chart :options="deadIncBarOption" class="stack-bar" />
  </div>
</template>
<script>
import cloneDeep from "lodash/cloneDeep.js";
// import moment from 'moment';
import ECharts from "vue-echarts";
import lineOption from "../chart-options/line";
import dayIncBarOption from "../chart-options/stack-bar";

export default {
  components: {
    "v-chart": ECharts
  },
  data() {
    return {
      lineOption,
      confirmedIncBarOption: cloneDeep(dayIncBarOption),
      suspectedIncBarOption: cloneDeep(dayIncBarOption),
      curedIncBarOption: cloneDeep(dayIncBarOption),
      deadIncBarOption: cloneDeep(dayIncBarOption),
      level: "city"
    };
  },
  computed: {},
  methods: {
    onConfirm() {
      console.log("onConfirm");
    },
    onSuspect() {
      console.log("onSuspect");
    },
    onCured() {
      console.log("onCured");
    },
    onDead() {
      console.log("onDead");
    },
    calcMax(dataList) {
      let max = dataList.reduce((prev, curr) => {
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
    updateLineTrend(dataList) {
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
    },
    queryDayLogs(level, area) {
      return this.$http
        .get(`/daylogs/${level}/${area}`)
        .then(response => {
          console.log("queryDayLogs success", response.data);
          let data = response.data;
          if (data.code != 0) {
            console.log("queryDayLogs success", data.msg);
            return;
          }
          let dataList = response.data.data;
          this.updateLineTrend(dataList);
          return dataList
        })
        .catch(res => {
          console.log("queryDayLogs failed", res);
        });
    },
    queryIncrementLogs(level, area) {
      return this.$http
        .get(`/incrementlogs/${level}/${area}`)
        .then(response => {
          console.log("queryIncrementLogs success", response.data);
          let data = response.data;
          if (data.code != 0) {
            console.log("queryIncrementLogs success", data.msg);
            return;
          }
          let dataList = response.data.data;
          // this.updateLineTrend(dataList);
          return dataList
        })
        .catch(res => {
          console.log("queryIncrementLogs failed", res);
        });
    },

    updateIncStackBar(totalDataList, incDataList, options, itemName){
      if( totalDataList.length == 0) return
      let dateList = totalDataList.map( item => item.updateTime)
      // let firstDay = moment(totalDataList[0].updateTime).add(-1, 'd').format('YYYY-MM-DD')
      // dateList.push(firstDay)

      let yDataList1 = totalDataList.map( item => item[itemName])
      yDataList1.unshift(0)
      let yDataList2 = incDataList.map( item => item[itemName])
      options.xAxis.data = dateList
      options.series[0].data = yDataList1
      options.series[1].data = yDataList2
    },
    queryData(level, area){
      Promise.all([this.queryDayLogs(level, area), this.queryIncrementLogs(level, area)])
        .then( res =>{
          console.log('queryData success', res)

          this.updateIncStackBar(...res, this.confirmedIncBarOption, 'confirmedCount')
          this.updateIncStackBar(...res, this.suspectedIncBarOption, 'suspectedCount')
          this.updateIncStackBar(...res, this.curedIncBarOption, 'curedCount')
          this.updateIncStackBar(...res, this.deadIncBarOption, 'deadCount')
        })
        .catch( res =>{
          console.log('queryData failed', res)

        })
    }
  },
  mounted() {
    this.confirmedIncBarOption.title.text = '每日新增确诊人数'
    this.suspectedIncBarOption.title.text = '每日新增疑似人数'
    this.curedIncBarOption.title.text = '每日新增治愈人数'
    this.deadIncBarOption.title.text = '每日新增死亡人数'
    this.queryData("country", "全球");
  }
};
</script>
<style lang='scss' scoped>
.line {
  margin-top: 20px;
  width: 750px;
  height: 550px;
}
.stack-bar {
  margin-top: 15px;
  width: 750px;
  height: 500px;
}
.title {
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
.data-type {
  margin: 15px 5px;
  .data-item {
    margin: 0 20px;
  }
}
</style>
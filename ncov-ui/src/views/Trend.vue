<template>
  <div>
    <div class="title">2019新冠肺炎趋势</div>
    <div>
      <div class="subtitle">区域范围</div>
    </div>
    <div class="area-type">
      <van-radio-group v-model="radio">
        <van-radio name="global" @click="onGlobalClick">
          <div class="area-whole">全球</div>
        </van-radio>
        <van-radio name="province">
          <van-field
            readonly
            clickable
            label="省份"
            :value="selectedProvince"
            placeholder="选择省份"
            @click="onProvinceInputClick"
          />
          <van-popup v-model="showProvincePicker" position="bottom">
            <van-picker
              show-toolbar
              :columns="provinceColumns"
              @cancel="showProvincePicker = false"
              @confirm="onProvinceConfirmed"
            />
          </van-popup>
        </van-radio>
        <van-radio name="city">
          <van-field
            readonly
            clickable
            label="城市"
            :value="selectedCity"
            placeholder="选择城市"
            @click="onCityInputClick"
          />
          <van-popup v-model="showCityPicker" position="bottom">
            <van-picker
              show-toolbar
              :columns="cityColumns"
              @cancel="showCityPicker = false"
              @confirm="onCityConfirmed"
            />
          </van-popup>
        </van-radio>
      </van-radio-group>
    </div>
    <div>
      <div class="subtitle">实时疫情</div>
      <van-icon name="replay" @click="onRefreshRealTime" />
      <div class="updatetime">更新时间 {{realTimeData.updateTime}}</div>
    </div>
    <div class="realtime">
      <div class="real-item">
        <div class="val confirmed">{{realTimeData.confirmedCount}}</div>
        <div class="label">确诊病例</div>
        <div>
          <div class="sub-label">今日</div>
          <div class="inc confirmed">+{{incrementData.confirmedCount}}</div>
        </div>
      </div>
      <div class="real-item">
        <div class="val suspected">{{realTimeData.suspectedCount}}</div>
        <div class="label">疑似病例</div>
        <div>
          <div class="sub-label">今日</div>
          <div class="inc suspected">+{{incrementData.suspectedCount}}</div>
        </div>
      </div>
      <div class="real-item">
        <div class="val cured">{{realTimeData.curedCount}}</div>
        <div class="label">治愈病例</div>
        <div>
          <div class="sub-label">今日</div>
          <div class="inc cured">+{{incrementData.curedCount}}</div>
        </div>
      </div>
      <div class="real-item">
        <div class="val dead">{{realTimeData.deadCount}}</div>
        <div class="label">死亡病例</div>
        <div>
          <div class="sub-label">今日</div>
          <div class="inc dead">+{{incrementData.deadCount}}</div>
        </div>
      </div>
    </div>
    <v-chart :options="lineOption" class="line" />
    <v-chart :options="confirmedIncBarOption" class="stack-bar" />
    <v-chart :options="suspectedIncBarOption" class="stack-bar" />
    <v-chart :options="curedIncBarOption" class="stack-bar" />
    <v-chart :options="deadIncBarOption" class="stack-bar" />
  </div>
</template>
<script>
import cloneDeep from "lodash/cloneDeep.js";
import { Toast } from "vant";
// import moment from 'moment';
import ECharts from "vue-echarts";
import "echarts/lib/chart/line";
import "echarts/lib/chart/lines";
import "echarts/lib/chart/bar";
import "echarts/lib/component/legend";
import "echarts/lib/component/title";
import "echarts/lib/component/dataset";
import "echarts/lib/component/tooltip";

import lineOption from "../chart-options/line";
import dayIncBarOption from "../chart-options/stack-bar";
import { colorDict, colorList } from "../map-data/colors.json";
import moment from "moment";

export default {
  components: {
    "v-chart": ECharts
  },
  data() {
    return {
      radio: "global",
      lineOption,
      confirmedIncBarOption: cloneDeep(dayIncBarOption),
      suspectedIncBarOption: cloneDeep(dayIncBarOption),
      curedIncBarOption: cloneDeep(dayIncBarOption),
      deadIncBarOption: cloneDeep(dayIncBarOption),
      realTimeData: {
        updateTime: moment().format("YYYY-MM-DD HH:mm"),
        confirmedCount: 0,
        suspectedCount: 0,
        curedCount: 0,
        deadCount: 0
      },
      incrementData: {
        confirmedCount: 0,
        suspectedCount: 0,
        curedCount: 0,
        deadCount: 0
      },
      selectedLevel: "country",
      selectedArea: "全球",
      selectedCity: "",
      selectedProvince: "",
      showCityPicker: false,
      showProvincePicker: false,
      areaList: [],
      cityColumns: [],
      provinceColumns: []
    };
  },
  computed: {},
  methods: {
    onRefreshRealTime() {
      this.queryData().finally(() => {
        Toast.success("刷新成功...");
      });
    },
    onGlobalClick() {
      this.selectedLevel = "country";
      this.selectedArea = "全球";
      this.queryData();
    },
    onCityInputClick() {
      this.selectedLevel = "city";
      if(this.cityColumns.length > 0){
        this.showCityPicker = true
        return 
      }
      this.queryAreasList(this.selectedLevel).then(res => {
        console.log("show city picker");
        this.cityColumns = res;
        this.showCityPicker = true;
      });
    },
    onProvinceInputClick() {
      console.log("onProvinceInputClick");
      this.selectedLevel = "province";
      if(this.provinceColumns.length > 0){
        this.showProvincePicker = true
        return
      }
      this.queryAreasList(this.selectedLevel).then(res => {
        console.log("show province picker");
        this.provinceColumns = res;
        this.showProvincePicker = true;
      });
    },
    onProvinceConfirmed(value) {
      console.log("onProvinceConfirmed", value);
      this.selectedProvince = value.text;
      this.selectedArea = value.text;
      this.queryData();
      this.showProvincePicker = false;
    },
    onCityConfirmed(values) {
      console.log("onCityConfirmed", values);
      this.selectedCity = values.join();
      this.selectedArea = values[1];
      this.queryData();
      this.showCityPicker = false;
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
      this.lineOption.series[0];
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
          return dataList;
        })
        .catch(res => {
          console.log("queryDayLogs failed", res);
        });
    },
    updateDataIncrement(dataList) {
      for (let item of dataList) {
        if (item.updateTime == moment().format("YYYY-MM-DD")) {
          this.incrementData = item;
          break;
        }
      }
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
          this.updateDataIncrement(dataList);
          return dataList;
        })
        .catch(res => {
          console.log("queryIncrementLogs failed", res);
        });
    },
    queryReadtimeData(level, area) {
      return this.$http
        .get(`/realtime/${level}/${area}`)
        .then(response => {
          console.log("queryReadtimeData success", response.data);
          this.realTimeData = response.data.data;
        })
        .catch(res => {
          console.log("queryReadtimeData failed", res);
        });
    },
    queryAreasList(level) {
      return this.$http
        .get("/arealist/" + level)
        .then(res => {
          console.log("queryAreasList success", res.data);
          let areaList = res.data.data;
          return areaList;
        })
        .catch(res => {
          console.log("queryAreasList fail", res.data);
        });
    },
    updateIncStackBar(totalDataList, incDataList, options, itemName) {
      if (totalDataList.length == 0) return;
      let dateList = totalDataList.map(item => item.updateTime);
      // let firstDay = moment(totalDataList[0].updateTime).add(-1, 'd').format('YYYY-MM-DD')
      // dateList.push(firstDay)

      let yDataList1 = totalDataList.map(item => item[itemName]);
      yDataList1.unshift(0);
      let yDataList2 = incDataList.map(item => item[itemName]);
      options.xAxis.data = dateList;
      options.series[0].data = yDataList1;
      options.series[1].data = yDataList2;
    },
    queryData() {
      return Promise.all([
        this.queryDayLogs(this.selectedLevel, this.selectedArea),
        this.queryIncrementLogs(this.selectedLevel, this.selectedArea),
        this.queryReadtimeData(this.selectedLevel, this.selectedArea)
      ])
        .then(res => {
          console.log("queryData success", res);

          this.updateIncStackBar(
            res[0],
            res[1],
            this.confirmedIncBarOption,
            "confirmedCount"
          );
          this.updateIncStackBar(
            res[0],
            res[1],
            this.suspectedIncBarOption,
            "suspectedCount"
          );
          this.updateIncStackBar(
            res[0],
            res[1],
            this.curedIncBarOption,
            "curedCount"
          );
          this.updateIncStackBar(
            res[0],
            res[1],
            this.deadIncBarOption,
            "deadCount"
          );
        })
        .catch(res => {
          console.log("queryData failed", res);
        });
    }
  },
  mounted() {
    this.lineOption.color = colorList;
    this.confirmedIncBarOption.title.text = "每日新增确诊人数";
    this.confirmedIncBarOption.series[1].itemStyle.color = colorDict.confirmed;
    this.suspectedIncBarOption.title.text = "每日新增疑似人数";
    this.suspectedIncBarOption.series[1].itemStyle.color = colorDict.suspected;
    this.curedIncBarOption.title.text = "每日新增治愈人数";
    this.curedIncBarOption.series[1].itemStyle.color = colorDict.cured;
    this.deadIncBarOption.title.text = "每日新增死亡人数";
    this.deadIncBarOption.series[1].itemStyle.color = colorDict.dead;
    // this.queryAreasList(this.selectedLevel);
    this.queryData();
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
  text-align: center;
}
.subtitle {
  display: inline-block;
  font-size: 32px;
  font-weight: bold;
  padding: 20px 5px;
  text-align: left;
  margin-left: 20px;
}
.updatetime {
  display: inline-block;
  padding-top: 20px;
  padding-right: 30px;
  float: right;
  font-size: 25px;
  color: rgb(100, 100, 100);
  text-align: right;
}
.area-type {
  margin: 20px;
  .area-whole {
    margin: 10px 10px 20px 30px;
    font-size: 28px;
    color: rgb(50, 50, 50);
  }
}
.data-type {
  margin: 15px 5px;
  .data-item {
    margin: 0 20px;
  }
}
.label {
  padding-top: 10px;
  color: rgb(70, 70, 70);
  font-size: 28px;
  font-weight: bold;
}
.realtime {
  border-radius: 20px;
  background-color: rgb(230, 230, 230);
  padding: 25px 0 10px 0;
  margin: 5px 20px;
  text-align: center;
  .real-item {
    display: inline-block;
    width: 150px;
    height: 100px;
    .val {
      font-size: 38px;
      font-weight: bold;
    }
    .inc {
      font-size: 20px;
      display: inline-block;
    }
    .sub-label {
      font-size: 20px;
      color: rgb(100, 100, 100);
      display: inline-block;
    }
    .confirmed {
      color: rgb(255, 12, 39);
    }
    .suspected {
      color: rgb(255,127,39);
    }
    .cured {
      color: rgb(0, 200, 15);
    }
    .dead {
      color: rgb(100, 100, 100);
    }
  }
}
</style>
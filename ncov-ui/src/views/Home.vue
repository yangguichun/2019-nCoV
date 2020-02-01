<template>
  <div>
    <div class="title">2020肺炎分布</div>
    <div class="date-picker">
      <van-button type="primary" size="small" @click="onPrevious">前一天</van-button>
      <div class="date-val">{{theDateStr}}</div>
      <van-button type="primary" size="small" @click="onNext">后一天</van-button>
    </div>
    <div class="data-type">
      <van-row>
        <val-col span="16">
          <van-tag round class="data-item" type="danger" @click="onConfirm">确诊</van-tag>
          <!-- <van-tag round class="data-item" type="primary" @click="onSuspect">疑似</van-tag> -->
          <van-tag round class="data-item" type="success" @click="onCured">治愈</van-tag>
          <van-tag round class="data-item" @click="onDead">死亡</van-tag>
        </val-col>
        <van-col span="8">
          <van-tag round class="data-item" type="primary" @click="onProvince">省份</van-tag>
          <van-tag round class="data-item" type="primary" @click="onCity">城市</van-tag>
        </van-col>
      </van-row>
    </div>
    <div class="area-type"></div>
    <v-chart :options="mapOption" class="map" />
    <v-chart :options="treeMapOption" class="treemap" />
  </div>
</template>
<script>
import moment from "moment";
import ECharts from "vue-echarts";
import chinaMap from "../map-data/china.json";
ECharts.registerMap("china", chinaMap);
import mapOption from "../chart-options/map";
import treeMapOption from "../chart-options/treemap";
import "echarts";

export default {
  components: {
    "v-chart": ECharts
  },
  data() {
    return {
      mapOption,
      treeMapOption,
      theDate: moment(),
      theDateStr: moment().format("YYYY-MM-DD"),
      minDate: moment("2020-01-24"),
      maxDate: moment(
        moment()
          .add(1, "d")
          .format("YYYY-MM-DD")
      ),
      dataName: "confirmedCount",
      selectedData: {
        name: "confirmedCount",
        color: "#ff0000"
      },
      level: "province"
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
    onConfirm() {
      console.log("onConfirm");
      this.treeMapOption.series[0].name = this.mapOption.title.text =
        "确诊人数";
      // this.mapOption.series[0].itemStyle.color = 'rgb(255,127,39)'
      this.mapOption.series[0].itemStyle.color = "rgb(255,12,39)";
      this.mapOption.series[0].symbolSize = val => {
        if(val[2] == 0) return 0
        let size = Math.min(val[2] / 15, 25);
        if (size < 2) size = 2;
        return size;
      };
      this.dataName = "confirmedCount";
      this.queryTheDateData();
    },
    onSuspect() {
      console.log("onSuspect");
      this.treeMapOption.series[0].name = this.mapOption.title.text =
        "疑似人数";
      this.mapOption.series[0].itemStyle.color = "rgb(13,94,242)";
      this.mapOption.series[0].symbolSize = val => {
        if(val[2] == 0) return 0
        let size = Math.min(val[2] / 15, 25);
        if (size < 2) size = 2;
        return size;
      };
      this.dataName = "suspectedCount";
      this.queryTheDateData();
    },
    onCured() {
      console.log("onCured");
      this.treeMapOption.series[0].name = this.mapOption.title.text =
        "治愈人数";
      this.mapOption.series[0].itemStyle.color = "rgb(0, 151, 15)";
      this.mapOption.series[0].symbolSize = val => {
        if(val[2] == 0) return 0
        let size = Math.min(val[2] / 3, 25);
        if (size < 2) size = 2;
        return size;
      };
      this.dataName = "curedCount";
      this.queryTheDateData();
    },
    onDead() {
      console.log("onDead");
      this.treeMapOption.series[0].name = this.mapOption.title.text =
        "死亡人数";
      this.mapOption.series[0].itemStyle.color = "rgb(100, 100, 100)";
      this.mapOption.series[0].symbolSize = val => {
        if(val[2] == 0) return 0
        let size = Math.min(val[2] / 3, 25);
        if (size < 2) size = 2;
        return size;
      };
      this.dataName = "deadCount";
      this.queryTheDateData();
    },
    onCity(){
      this.level = 'city'
      this.queryTheDateData();
    },
    onProvince(){
      this.level = 'province'
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
          let formatedMapDataList = dataList.map(item => {
            return {
              name: item.name,
              value: [item.lng, item.lat, item[this.dataName]]
            };
          });
          let formatedMapTreeData = dataList.map(item => {
            if (item[this.dataName] > 0) {
              console.log("大于1的数量", item.name, item[this.dataName]);
            }
            return {
              name: item.name,
              path: item.name,
              value: item[this.dataName]
            };
          });

          this.mapOption.series[0].data = formatedMapDataList;
          console.log("formatedMapTreeData", formatedMapTreeData);
          this.treeMapOption.series[0].data = formatedMapTreeData;
        })
        .catch(res => {
          console.log("queryTheDateData fail", res.data);
        });
    }
  },
  mounted() {
    this.queryTheDateData();
  }
};
</script>
<style lang='scss' scoped>
.map {
  width: 750px;
  height: 500px;
}
.treemap {
  margin-top: 5px;
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
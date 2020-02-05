<template>
  <div>
    <div class="title">2019新冠肺炎分布</div>
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
import "echarts/lib/chart/scatter";
import "echarts/lib/chart/effectScatter";
import "echarts/lib/chart/treemap";
import "echarts/lib/chart/map";
import "echarts/lib/component/geo";
import "echarts/lib/component/legend";
import "echarts/lib/component/title";
import "echarts/lib/component/visualMap";
import "echarts/lib/component/dataset";
import "echarts/lib/component/tooltip";

import chinaMap from "../map-data/china.json";
ECharts.registerMap("china", chinaMap);
import mapOption from "../chart-options/map";
import treeMapOption from "../chart-options/treemap";
import { colorDict } from "../map-data/colors.json";
// import "echarts";

let selectedOptionsList = {
  confirmed: {
    itemName: "confirmedCount",
    label: "确诊人数",
    color: colorDict.confirmed,
    sizeDevider: 15
  },
  suspected: {
    itemName: "suspectedCount",
    label: "疑似人数",
    color: colorDict.suspected,
    sizeDevider: 3
  },
  cured: {
    itemName: "curedCount",
    label: "治愈人数",
    color: colorDict.cured,
    sizeDevider: 3
  },
  dead: {
    itemName: "deadCount",
    label: "死亡人数",
    color: colorDict.dead,
    sizeDevider: 3
  }
};
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
      selectedOption: selectedOptionsList.confirmed,
      level: "province",
      devideSize: 10
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
    updateOptionAndQuery() {
      this.queryTheDateData().then(() => {
        this.treeMapOption.series[0].name = this.mapOption.title.text = `${this.selectedOption.label}(${this.level})`;
        this.mapOption.series[0].itemStyle.color = this.selectedOption.color;
        this.mapOption.series[0].symbolSize = val => {
          if (val[2] == 0) return 0;
          let size = Math.min(val[2] / this.selectedOption.sizeDevider, 25);
          if (size < 2) size = 2;
          return size;
        };
      });
    },
    onConfirm() {
      console.log("onConfirm");
      this.selectedOption = selectedOptionsList.confirmed;
      this.updateOptionAndQuery();
    },
    // onSuspect() {
    //   console.log("onSuspect");
    //   this.treeMapOption.series[0].name = this.mapOption.title.text = `疑似人数(${this.level})`;
    //   this.mapOption.series[0].itemStyle.color = "rgb(255,127,39)";
    //   this.mapOption.series[0].symbolSize = val => {
    //     if (val[2] == 0) return 0;
    //     let size = Math.min(val[2] / 15, 25);
    //     if (size < 2) size = 2;
    //     return size;
    //   };
    //   this.dataName = "suspectedCount";
    //   this.queryTheDateData();
    // },
    onCured() {
      console.log("onCured");
      this.selectedOption = selectedOptionsList.cured;
      this.updateOptionAndQuery();
    },
    onDead() {
      console.log("onDead");
      this.selectedOption = selectedOptionsList.dead;
      this.updateOptionAndQuery();
    },
    onCity() {
      this.level = "city";
      this.treeMapOption.series[0].name = this.mapOption.title.text = `${this.selectedOption.label}(${this.level})`;
      this.queryTheDateData();
    },
    onProvince() {
      this.level = "province";
      this.treeMapOption.series[0].name = this.mapOption.title.text = `${this.selectedOption.label}(${this.level})`;

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
    convertToMapTreeData(dataList) {
      let total = dataList.reduce((pre, curr) => {
        return pre + curr[this.selectedOption.itemName];
      }, 0);

      let formatedMapTreeData = dataList.map(item => {
        let children = [];
        if (item.children) {
          let subTotal = item.children.reduce((pre, curr) => {
            return pre + curr[this.selectedOption.itemName];
          }, 0);
          children = item.children.map(subItem => {
            return {
              name: subItem.name,
              value: subItem[this.selectedOption.itemName],
              total: subTotal
            };
          });
        }
        return {
          name: item.name,
          value: item[this.selectedOption.itemName],
          total: total,
          children: children
        };
      });
      return formatedMapTreeData;
    },
    calcSizeDevider(dataList, itemName) {
      let countList = dataList.map( item => item[itemName]);
      countList.sort((a, b) => b - a);
      let res = 15
      if (countList.length > 3) {
        res = countList[2] / 25.0;
      }
      console.log('calcSizeDevider1', res)
      if( res < 0.5){
        res = 0.5
      }
      console.log('calcSizeDevider2', res)
      return res
    },
    queryTheDateData() {
      return this.$http
        .get(`/allareadata/${this.level}/${this.theDateStr}`)
        .then(res => {
          console.log("queryTheDateData success", res.data);
          let data = res.data;
          if (data.code != 0) {
            console.log("queryTheDateData fail, ", data);
            return;
          }
          let dataList = res.data.data;
          if(this.theDateStr == moment().format('YYYY-MM-DD')){
            this.selectedOption.sizeDevider = this.calcSizeDevider(dataList, this.selectedOption.itemName);
          }
          let formatedMapDataList = dataList.map(item => {
            return {
              name: item.name,
              value: [item.lng, item.lat, item[this.selectedOption.itemName]]
            };
          });
          this.mapOption.series[0].data = formatedMapDataList;

          let formatedMapTreeData = this.convertToMapTreeData(dataList);
          this.treeMapOption.series[0].data = formatedMapTreeData;
        })
        .catch(res => {
          console.log("queryTheDateData fail", res.data);
        });
    }
  },
  mounted() {
    this.updateOptionAndQuery();
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
  text-align: center;
}
.date-picker {
  margin: 15px 5px;
  text-align: center;
  .date-val {
    display: inline-block;
    padding: 5px 30px;
  }
}
.data-type {
  margin: 25px 5px 15px 5px;
  text-align: center;
  .data-item {
    margin: 0 20px;
  }
}
</style>
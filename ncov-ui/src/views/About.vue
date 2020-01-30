<template>
  <div>
    <van-button type="default">默认按钮</van-button>
    <v-chart :options="mapData" class="map"/>
  </div>
</template>
<script>
import ECharts from "vue-echarts";
import chinaMap from '../map-data/china.json'
ECharts.registerMap('china', chinaMap)
import mapData from '../chart-options/map'
import "echarts";

export default {
  components: {
    "v-chart": ECharts
  },
  data() {
    return {
      mapData
    }
  },
  computed: {
  }
};
</script>
<style lang='scss' scoped>
.map{
  width: 750px;
  height:400px;
}
</style>
<template>
  <div >
    <v-chart :options="mapData" style="width: 100%;height:350px;"/>
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
</style>
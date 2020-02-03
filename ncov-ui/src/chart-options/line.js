export default {
  title: {
    text: "总数趋势",
    textStyle:{
      fontSize: 15
    },
    left: 10,
    top: 15,
  },
  tooltip: {
    trigger: "axis",
    formatter: function(params) {
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
    top: "5%"
  },
  grid: {
    show: true,
    left: "3%",
    right: "3%",
    bottom: "0%",
    top: "20%",
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
      hoverAnimation: false,
      data: []
    },
    {
      name: "疑似",
      type: "line",
      hoverAnimation: false,
      data: []
    },
    {
      name: "治愈",
      type: "line",
      hoverAnimation: false,
      data: []
    },
    {
      name: "死亡",
      type: "line",
      hoverAnimation: false,
      data: []
    }
  ]
}
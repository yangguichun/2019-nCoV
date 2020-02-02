// import echarts from 'echarts'

export default {
  backgroundColor: '#eeeeee',
  title: {
    text: '确诊人数(province)',
    left: 'center',
    textStyle: {
      color: '#333333'
    },
    top:10
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    y: 'bottom',
    x: 'right',
    data: ['人数'],
    textStyle: {
      color: '#fff'
    }
  },
  geo: {
    map: 'china',
    silent:true,
    roam: true,
    zoom: 1.2,
    label: {
      emphasis: {
        show: false
      }
    },
    itemStyle: {
      normal: {
        areaColor: '#f7f8fa',
        borderColor: '#888888',
      },
      emphasis: {
        areaColor: '#2a333d'
      }
    }
  },
  series: [
    {
      name: '人数',
      type: 'scatter',
      coordinateSystem: 'geo',
      data: [],
      symbolSize: val => {
        if(val[2] == 0) return 0
        let size = Math.min(val[2] / 15, 25)
        if (size < 2) size = 2
        return size;
      },
      tooltip: {
        formatter: function (val) {
          return val.name + ': ' + val.value[2]
        }
      },
      itemStyle: {
        color: 'rgb(255,12,39)',
        opacity: 0.8
      }
      // new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
      //   offset: 0,
      //   color: 'rgb(129, 227, 238)'
      // }, {
      //   offset: 1,
      //   color: 'rgb(25, 183, 207)'
      // }])
    },
    {
      name: 'Top 5',
      type: 'effectScatter',
      coordinateSystem: 'geo',
      data: [],
      symbolSize: val => val[2] / 10,
      showEffectOn: 'render',
      rippleEffect: {
        brushType: 'stroke'
      },
      hoverAnimation: true,
      tooltip: {
        formatter: function (val) {
          return val.name + ': ' + val.value[2]
        }
      },
      label: {
        normal: {
          formatter: '{b}',
          position: 'right',
          show: true
        }
      },
      itemStyle: {
        normal: {
          color: '#f4e925',
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      zlevel: 1
    }
  ]
}

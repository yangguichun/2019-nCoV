import echarts from 'echarts'

var formatUtil = echarts.format;

function getLevelOption() {
  return [
    {
      itemStyle: {
        borderWidth: 0,
        gapWidth: 5
      }
    },
    {
      itemStyle: {
        gapWidth: 1
      }
    },
    {
      colorSaturation: [0.35, 0.5],
      itemStyle: {
        gapWidth: 1,
        borderColorSaturation: 0.6
      }
    }
  ];
}

export default {
  // title: {
  //   text: 'Disk Usage',
  //   left: 'center'
  // },
  tooltip: {
    formatter: function (info) {
      var value = info.value;
      var treePathInfo = info.treePathInfo;
      var treePath = [];

      for (var i = 1; i < treePathInfo.length; i++) {
        treePath.push(treePathInfo[i].name);
      }

      return [
        '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('/')) + '</div>',
        '人数 ' + formatUtil.addCommas(value),
      ].join('');
    }
  },

  series: [
    {
      name: '确诊分布',
      type: 'treemap',
      visibleMin: 1,
      top:10,
      left:5,
      right:5,
      bottom:5,
      label: {
        show: true,
        formatter: '{b}'
      },
      itemStyle: {
        borderColor: '#fff'
      },
      levels: getLevelOption(),
      data: []
    }
  ]
}
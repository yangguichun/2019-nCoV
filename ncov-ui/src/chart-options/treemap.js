import * as formatUtil from 'echarts/lib/util/format'

function getLevelOption() {
  return [
    {
      itemStyle: {
        borderWidth: 0,
        gapWidth: 2
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
    show: true,
    formatter: function (info) {
      console.log('treemap formatter', info)
      var value = info.value;
      var treePathInfo = info.treePathInfo;
      var treePath = [];

      for (var i = 1; i < treePathInfo.length; i++) {
        treePath.push(treePathInfo[i].name);
      }
      let res = [
        '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('/')) + '</div>',
        '人数 ' + formatUtil.addCommas(value) +'<br>',
        '比例 ' + (value/info.data.total*100).toFixed(0) + '%'
      ].join('');
      return res;
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
      leafDepth: 1,
      data: []
    }
  ]
}
export default {
    title: {
        text: '每日增量',
        textStyle: {
            fontSize: 15
        },
        top: 15,
        left: 10
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        },
        formatter: function (params) {
            if (isNaN(params[2].value)) {
                //如果是增加
                return `${params[0].name}<br/>${params[0].seriesName}: ${params[0].value + params[1].value}<br/>${params[1].seriesName}: ${params[1].value}`
            } else {
                //如果是减少
                return `${params[0].name}<br/>${params[0].seriesName}: ${params[0].value}<br/>${params[2].seriesName}: ${params[2].value}`
            }
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
        top: "5%",
        right: "5%",
        data: ['增加', '下降']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        splitLine: { show: false },
        data: function () {
            var list = [];
            for (var i = 1; i <= 11; i++) {
                list.push('11月' + i + '日');
            }
            return list;
        }()
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '总数',
            type: 'bar',
            stack: '参数1',
            itemStyle: {
                barBorderColor: 'rgba(0,0,0,0)',
                color: 'rgba(0,255,0,0)'
            },
            emphasis: {
                itemStyle: {
                    barBorderColor: 'rgba(0,0,0,0)',
                    color: 'rgba(0,0,0,0)'
                }
            },
            data: [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292]
        },
        {
            name: '增加',
            type: 'bar',
            stack: '参数1',
            label: {
                show: true,
                position: 'top'
            },
            itemStyle: {
                color: 'rgba(200,0,0)'
            },
            data: [900, 345, 393, '-', '-', 135, 178, 286, '-', '-', '-']
        },
        {
            name: '下降',
            type: 'bar',
            stack: '参数1',
            label: {
                show: true,
                position: 'bottom'
            },
            itemStyle: {
                color: 'rgba(200,200,200)'
            },
            data: ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
        },
        // {
        //     name: '辅助2',
        //     type: 'bar',
        //     stack: '参数2',
        //     itemStyle: {
        //         barBorderColor: 'rgba(0,0,0,0)',
        //         color: 'rgba(0,255,0,0)'
        //     },
        //     emphasis: {
        //         itemStyle: {
        //             barBorderColor: 'rgba(0,0,0,0)',
        //             color: 'rgba(0,0,0,0)'
        //         }
        //     },
        //     data: [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292]
        // },
        // {
        //     name: '增量2',
        //     type: 'bar',
        //     stack: '参数2',
        //     label: {
        //         show: true,
        //         position: 'top'
        //     },
        //     data: [900, 345, 393, '-', '-', 135, 178, 286, '-', '-', '-']
        // },
    ]
}

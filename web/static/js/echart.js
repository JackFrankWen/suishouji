function pieInit() {
        var myChart = echarts.init(document.getElementById('pie-chart'));
                          // 指定图表的配置项和数据
                          var option = {
                              title: {
                                text: '月账单',
                                left: 'center',
                                top: 'center'
                              },
                              series: [
                                {
                                  radius: ['40%', '70%'],
                                  type: 'pie',
                                  data: [
                                    {
                                      value: 335,
                                      name: '吃喝'
                                    },
                                    {
                                      value: 335,
                                      name: '购物消费'
                                    },
                                    {
                                      value: 234,
                                      name: '宝宝消费'
                                    },
                                    {
                                      value: 234,
                                      name: '联盟广告'
                                    },
                                    {
                                      value: 1548,
                                      name: '搜索引擎'
                                    }
                                  ]
                                }
                              ]
                            };
                          // 使用刚指定的配置项和数据显示图表。
                          myChart.setOption(option);
}
function barInit() {
        var myChart = echarts.init(document.getElementById('bar-chart'));
                          // 指定图表的配置项和数据
                          var option = {
                              xAxis: {
                                data: ['一月', '二月', '三月', '四月', '五月', '六月', '七月','八月','九月','十月','十月','十二月']
                              },
                              yAxis: {},
                              series: [
                                {
                                  type: 'bar',
                                  data: new Array(12).fill(getRandomInt(22))
                                }
                              ]
                            };
                          // 使用刚指定的配置项和数据显示图表。
                          myChart.setOption(option);
}
function lineInit() {
        var myChart = echarts.init(document.getElementById('line-chart'));
                          // 指定图表的配置项和数据
                          var option = {
                              xAxis: {
                                type: 'category',
                                data: ['A', 'B', 'C']
                              },
                              yAxis: {
                                type: 'value'
                              },
                              series: [
                                {
                                  data: [120, 200, 150],
                                  type: 'line'
                                }
                              ]
                            };
                          // 使用刚指定的配置项和数据显示图表。
                          myChart.setOption(option);
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}
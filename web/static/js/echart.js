function pieInit(data =[]) {
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
                                  data: data
                                }
                              ]
                            };
                          // 使用刚指定的配置项和数据显示图表。
                          myChart.setOption(option);
}
function barInit(data ={}) {
        var myChart = echarts.init(document.getElementById('bar-chart'));
                          // 指定图表的配置项和数据
                          var option = {
                              xAxis: {
                                data: __enum.monthToCH(data.label)
                              },
                              yAxis: {},
                              series: [
                                {
                                  type: 'bar',
                                  label:{
                                      show:true,
                                      formatter: (val)=>{
                                          return __utils.numFormat(val.value,true)
                                      }
                                  },
                                  data: data.value
                                }
                              ]
                            };
                          // 使用刚指定的配置项和数据显示图表。
                          myChart.setOption(option);
}
function lineInit(data) {
        var myChart = echarts.init(document.getElementById('line-chart'));
                          // 指定图表的配置项和数据
                          var option = {
                              xAxis: {
                                type: 'category',
                                data: __enum.monthToCH(data.label)
                              },
                              yAxis: {
                                type: 'value'
                              },
                              series: [
                                {
                                  data: data.value,
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
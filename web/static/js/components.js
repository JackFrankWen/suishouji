  Vue.component('table-expend-list', {
              props: ['data', 'redirectClick'],
              template: `<div style="margin: -12px">
                        <tr v-for="item in data" class="row align-items-center bg-light border-bottom" @click="$emit('redirect-to-tab', item)">
                            <span style="width: 48px" class="bg-light p-2"></span>
                            <span class="col bg-light p-2"></span>
                            <span class="col p-2 bg-secondary text-white">{{ item.label }}</span>
                            <span class="col bg-light p-2 ">{{ __utils.numFormat(item.amount) }}</span>
                          </tr>
                        </div>`
  })
  Vue.component('bookkeep-alert', {
              props: ['data'],
              template: ` <el-alert
                        title="标签规则"
                        type="warning"
                        show-icon>
                          <slot>
                              <ul>
                                  <li>1.日常支出（买菜，沃尔玛，工作餐）消费频率基本每月正常需求类需求</li>
                                  <li> 2.变动支出（零食，购物衣服）特殊消费其他支出，包括医疗、学习、美容、不知道该怎么记的烂账等等</li>
                                  <li>   3.固定支出（水电煤，加油费，理发，话费各种年费会员费必须要消费，消费周期可能两三个月缴费）"</li>
                              </ul>
                          </slot>
                      </el-alert>`
  })

  Vue.component('bookkeep-alert-rule', {
              props: ['data'],
              template: ` <el-alert
                        title="分类规则"
                        type="warning"
                        show-icon>
                          <slot>
                              <ul>
                                  <li>1.【食品】零食（美团，夜宵，）工作餐（正常早午晚餐）</li>
                                  <li>2.【购物消费】日常用品（卫生纸，日常消耗品），厨房用品</li>
                                  <li>3.【家庭杂费】（水电煤，加油费，理发，话费各种年费会员费） </li>
                              </ul>
                          </slot>
                      </el-alert>`
  })
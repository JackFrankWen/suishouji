  Vue.component('table-expend-list', {
              props: ['data'],
              template: `<div>
                        <tr v-for="item in data" class="row align-items-center">
                            <span style="width: 48px"></span>
                            <span class="col"></span>
                            <span class="col">{{ item.label }}</span>
                            <span class="col">{{ __utils.numFormat(item.amount) }}</span>
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
                                  <li>1.日常消费（买菜，沃尔玛，工作餐）正常需求类需求</li>
                                  <li> 2.一次性消费（零食，购物衣服）其他支出，包括医疗、学习、美容、不知道该怎么记的烂账等等</li>
                                  <li>   3.固定消费（水电煤，加油费，理发，话费各种年费会员费）"</li>
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
                                  <li>2.【购物消费】日常用品（卫生纸，）， 厨房用品</li>
                                  <li>3.【家庭杂费】（水电煤，加油费，理发，话费各种年费会员费）
                                  </li>
                              </ul>
                          </slot>
                      </el-alert>`
  })
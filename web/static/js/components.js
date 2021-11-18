  Vue.component('table-expend-list', {
              props: ['data'],
              template: `<div>
                        <tr v-for="item in data" class="row align-items-center">
                            <span style="width: 48px"></span>
                            <span class="col"></span>
                            <span class="col">{{ item.label }}</span>
                            <span class="col">{{ item.amount }}</span>
                          </tr>
                        </div>`
  })
// account_type INT COMMENT '消费账户 1.老公钱包 2.老婆钱包 3，爷爷钱包 ',
//     payment_type INT COMMENT '付款类型 1.支付宝 2.微信 3.银行卡 4.现金',
//     customer INT COMMENT '消费对象 1.家庭 2.老公 3.老婆 4.牧 ',
//     tag INT COMMENT '标签 1.日常消费（买菜，沃尔玛） 2.一次性消费（零食，购物衣服） 3.固定消费（水电煤，油费，理发话费）'
const general_consumer = 1, one_off_consumer = 2, fix_consumer = 3;
const husband = 1, wife = 2, family = 3, son = 4;
const __enum = {
    accountType: {
        1: '老公钱包',
        2: '老婆钱包',
        3: '爷爷钱包'
    },
    paymentType: {
        1: '支付宝',
        2: '微信',
        3: '银行卡',
        4: '现金'
    },
    consumer: {
        1: '老公',
        2: '老婆',
        3: '家庭',
        4: '牧牧'
    },
    tag: {
        1: '日常消费',
        2: '一次性消费',
        3: '固定消费'
    },
    transform: function (obj) {
        return Object.keys(obj).map(
            (key) => ({label: obj[key], value: Number(key)})
            )
    },
    safeMapping: function (key, obj) {
        if (obj.hasOwnProperty(key)) {
            return obj[key]
        }
        return ''
    },
    getConsumerKey: function(key){
        return this.safeMapping(key, this.consumer)
    },
    getAccountTypeKey: function(key){
        return this.safeMapping(key, this.accountType)
    },
    getPaymentTypeKey: function(key){
         return this.safeMapping(key, this.paymentType)
    },
    getTagKey: function(key){
        return this.safeMapping(key, this.tag)
    },
    getConsumer: function(){
        return this.transform(this.consumer)
    },
    getAccountType: function(){
        return this.transform(this.accountType)
    },
    getPaymentType: function(){
        return this.transform(this.paymentType)
    },
    getTag: function(){
        return this.transform(this.tag)
    },
    getCategoryObj: function(){
        const obj = {};
        this.categoryType.forEach((item,index)=>{
            obj[item.value] = item.label;
            item.children.forEach((item)=>{
                 obj[item.value] = item.label;
            })
        })
        return obj
    },
    getCategoryMappingRule: function(){
        const obj = {};
        this.categoryType.forEach((item,index)=>{
            item.children.forEach((item)=>{
                 obj[item.value] = item;
            })
        })
        return obj
    },
    getCategoryLabel: function(json) {
        if (json) {
            const obj =  this.getCategoryObj();
            const arr = JSON.parse(json)
            return obj[arr[1]]
        }
    },
    categoryType: [{
                  value: 10000,
                  label: '食品(吃喝)',
                  children: [{
                    value: 10001,
                    label: '买菜',
                      tag: general_consumer,
                      consumer: family,
                  }, {
                    value: 10002,
                    label: '超市',
                       tag: general_consumer,
                      consumer: family,
                  }, {
                    value: 10003,
                    label: '水果',
                       tag: general_consumer,
                      consumer: family,
                  }, {
                    value: 10004,
                    label: '零食（宵夜）',
                      tag: one_off_consumer,
                  }, {
                    value: 10005,
                    label: '工作餐（早午晚）',
                      tag: general_consumer,
                  }, {
                    value: 10006,
                    label: '下馆子',
                       tag: one_off_consumer,
                      consumer: family,
                  }]
                 }, {
                  value: 50000,
                  label: '购物消费',
                  children: [{
                    value: 50001,
                    label: '衣裤鞋帽',
                       tag: one_off_consumer,
                  }, {
                    value: 50002,
                    label: '日常用品',
                      tag: fix_consumer,
                      consumer: family,
                  }, {
                    value: 50003,
                    label: '电子数码',
                        tag: one_off_consumer,
                  }, {
                    value: 50004,
                    label: '厨房用品',
                      tag: fix_consumer,
                      consumer: family,
                  }, {
                    value: 50005,
                    label: '化妆美容品',
                      tag: one_off_consumer,
                      consumer: wife,
                  }, {
                    value: 50006,
                    label: '宠物支出',
                      tag: fix_consumer,
                      consumer: family,
                  }, {
                    value: 50007,
                    label: '汽车用品',
                        tag: one_off_consumer,
                      consumer: family,
                  }, {
                    value: 50008,
                    label: '家具家电',
                      tag: fix_consumer,
                      consumer: family,
                  }]
                }, {
                  value: 20000,
                  label: '家庭杂费',
                  children: [{
                    value: 20001,
                    label: '水费',
                       tag: general_consumer,
                      consumer: family,
                  }, {
                    value: 20002,
                    label: '电费',
                       tag: general_consumer,
                      consumer: family,
                  }, {
                    value: 20003,
                    label: '燃气费',
                       tag: general_consumer,
                      consumer: family,
                  }, {
                    value: 20004,
                    label: '物业费',
                       tag: fix_consumer,
                      consumer: family,
                  }, {
                    value: 20005,
                    label: '快递费',
                      tag: general_consumer,
                  }, {
                    value: 20006,
                    label: '理发费',
                      tag: fix_consumer,
                  }, {
                    value: 20007,
                    label: '手机话费',
                        tag: fix_consumer,
                  }, {
                    value: 20008,
                    label: 'VPN年费',
                      tag: fix_consumer,
                  }]
                }, {
                  value: 40000,
                  label: '宝宝费用',
                  children: [{
                    value: 40001,
                    label: '宝宝尿不湿',
                       tag: fix_consumer,
                      consumer: son,
                  }, {
                    value: 40002,
                    label: '宝宝玩具',
                      tag: one_off_consumer,
                      consumer: son,
                  }, {
                    value: 40003,
                    label: '宝宝教育',
                      tag: fix_consumer,
                      consumer: son,
                  }, {
                    value: 40004,
                    label: '宝宝医疗',
                      tag: one_off_consumer,
                      consumer: son,
                  }, {
                    value: 40005,
                    label: '宝宝生活用品',
                      tag: fix_consumer,
                      consumer: son,
                  }, {
                    value: 40006,
                    label: '宝宝衣物',
                      tag: one_off_consumer,
                      consumer: son,
                  }, {
                    value: 40007,
                    label: '宝宝食品',
                      tag: one_off_consumer,
                      consumer: son,
                  }]
                }, {
                  value: 30000,
                  label: '行车交通',
                  children: [{
                    value: 30001,
                    label: '违章罚款',
                  }, {
                    value: 30002,
                    label: '地铁公交',
                         tag: general_consumer,
                  }, {
                    value: 30003,
                    label: '打车',
                       tag: general_consumer,
                  }, {
                    value: 30004,
                    label: '火车飞机等',
                       tag: one_off_consumer,
                  }, {
                    value: 30005,
                    label: '停车费',
                       tag: general_consumer,
                  }]
                }, {
                  value: 60000,
                  label: '人情费用',
                  children: [{
                    value: 60001,
                    label: '请客',
                      tag: one_off_consumer,
                  }, {
                    value: 60002,
                    label: '回礼',
                      tag: one_off_consumer,
                  }, {
                    value: 60003,
                    label: '孝敬长辈',
                      tag: one_off_consumer,
                  }]
                }, {
                  value: 70000,
                  label: '休闲娱乐',
                  children: [{
                    value: 70001,
                    label: '聚会',
                      tag: one_off_consumer,
                  }, {
                    value: 70002,
                    label: '游戏（桌游）',
                      tag: one_off_consumer,
                  }, {
                    value: 70003,
                    label: '其他娱乐',
                      tag: one_off_consumer,
                  }]
                }, {
                  value: 80000,
                  label: '保险医疗',
                  children: [{
                    value: 80001,
                    label: '个人保险',
                      tag: fix_consumer,
                  }, {
                    value: 80002,
                    label: '医疗费用',
                      tag: one_off_consumer,
                  }, {
                    value: 80003,
                    label: '医疗杂物',
                      tag: fix_consumer,
                  }]
                }, {
                  value: 90000,
                  label: '个人投资',
                  children: [{
                    value: 90001,
                    label: '摄影',
                      tag: one_off_consumer,
                  }, {
                    value: 90002,
                    label: '书包杂志',
                      tag: one_off_consumer,
                  }, {
                    value: 90003,
                    label: '个人投资',
                      tag: one_off_consumer,
                  }]
                }, {
                  value: '00000',
                  label: '未分类',
                  children: []
                }
    ],
}

pickerOptions = {
                      shortcuts: [{
                        text: '本月',
                        onClick(picker) {
                            const date = new Date(), y = date.getFullYear(), m = date.getMonth();
                            const firstDay = new Date(y, m, 1);
                            const lastDay = new Date(y, m+1, 0);
                            picker.$emit('pick', [firstDay, lastDay]);
                        }
                      }, {
                        text: '上个月',
                        onClick(picker) {
                            const date = new Date(), y = date.getFullYear(), m = date.getMonth();
                            const firstDay = new Date(y, m-1, 1);
                            const lastDay = new Date(y, m, 0);
                          picker.$emit('pick', [firstDay, lastDay]);
                        }
                      }]
                    }
__init = {
    formTransaction() {
        return {
                  create_time: undefined,
                  category: undefined,
                  consumer: undefined,
                  payment_type: undefined,
                  amount: undefined,
                  account_type: undefined,
                  tag: undefined,
                  description: undefined,
                    action: 1,//1 新建 2 修改
                }
    },
    formTransactionRule() {
        return {
                  create_time: [ { required: true, message: '必填', trigger: 'change' }],
                  category: [{ required: true, message: '必填', trigger: 'change' }],
                  consumer: [{ required: true, message: '必填', trigger: 'change' }],
                  payment_type: [{ required: true, message: '必填', trigger: 'change' }],
                  amount: [{ required: true, message: '必填', trigger: 'change' }],
                  account_type: [{ required: true, message: '必填', trigger: 'change' }],
                  tag: [{ required: true, message: '必填', trigger: 'change' }],
                  description: [{ required: true, message: '必填', trigger: 'change' }],
                }
    },
    batchUpdateForm() {
        return  {// 查账
                    paymentType: undefined,
                    accountType: undefined,
                    consumer: undefined,
                }
    },
    formUpload() {
        return { // 入账
                    accountType: undefined,// 消费账户
                    paymentType: undefined,
                    consumer: undefined,
                    fileList: [],
                }
    },
    drawerForm() {
        return {
                    category: undefined,
                    tag: undefined,
                    rule: undefined,
                    consumer: undefined,
                }
    },
    formInline() {
        return  {// 查账
                    picker: undefined,
                    paymentType: undefined,
                    accountType: undefined,
                    consumer: undefined,
                    pickerOptions: pickerOptions,
                }
    },
    batchQueryForm() {
        return {// 查账
                    picker: undefined,
                    paymentType: undefined,
                    accountType: undefined,
                    consumer: undefined,
                    description: undefined,
                    query_null: 1,
                    pickerOptions: pickerOptions,
                }
    },

}



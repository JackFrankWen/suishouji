// account_type INT COMMENT '消费账户 1.老公钱包 2.老婆钱包 3，爷爷钱包 ',
//     payment_type INT COMMENT '付款类型 1.支付宝 2.微信 3.银行卡 4.现金',
//     customer INT COMMENT '消费对象 1.家庭 2.老公 3.老婆 4.牧 ',
//     tag INT COMMENT '标签 1.日常消费（买菜，沃尔玛） 2.一次性消费（零食，购物衣服） 3.固定消费（水电煤，油费，理发话费）'

var __enum = {
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
        0: '未分类',
        1: '家庭',
        2: '老公',
        3: '老婆',
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
                  }, {
                    value: 10002,
                    label: '超市',
                  }, {
                    value: 10003,
                    label: '水果',
                  }, {
                    value: 10004,
                    label: '零食（宵夜）',
                  }, {
                    value: 10005,
                    label: '工作餐（早午晚）',
                  }, {
                    value: 10006,
                    label: '下馆子',
                  }]
                 }, {
                  value: 50000,
                  label: '购物消费',
                  children: [{
                    value: 50001,
                    label: '衣裤鞋帽',
                  }, {
                    value: 50002,
                    label: '日常用品',
                  }, {
                    value: 50003,
                    label: '电子数码',
                  }, {
                    value: 50004,
                    label: '厨房用品',
                  }, {
                    value: 50005,
                    label: '化妆品',
                  }, {
                    value: 50006,
                    label: '宠物支出',
                  }, {
                    value: 50007,
                    label: '汽车用品',
                  }, {
                    value: 50008,
                    label: '家具家电',
                  }]
                }, {
                  value: 20000,
                  label: '家庭杂费',
                  children: [{
                    value: 20001,
                    label: '水费',
                  }, {
                    value: 20002,
                    label: '电费',
                  }, {
                    value: 20003,
                    label: '燃气费',
                  }, {
                    value: 20004,
                    label: '物业费',
                  }, {
                    value: 20005,
                    label: '快递费',
                  }, {
                    value: 20006,
                    label: '理发费',
                  }, {
                    value: 20007,
                    label: '手机话费',
                  }, {
                    value: 20008,
                    label: 'VPN年费',
                  }]
                }, {
                  value: 40000,
                  label: '宝宝费用',
                  children: [{
                    value: 40001,
                    label: '宝宝尿不湿',
                  }, {
                    value: 40002,
                    label: '宝宝玩具',
                  }, {
                    value: 40003,
                    label: '宝宝教育',
                  }, {
                    value: 40004,
                    label: '宝宝医疗',
                  }, {
                    value: 40005,
                    label: '宝宝生活用品',
                  }, {
                    value: 40006,
                    label: '宝宝衣物',
                  }, {
                    value: 40007,
                    label: '宝宝食品',
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
                  }, {
                    value: 30003,
                    label: '打车',
                  }, {
                    value: 30004,
                    label: '火车飞机等',
                  }, {
                    value: 30005,
                    label: '停车费',
                  }]
                }, {
                  value: 60000,
                  label: '人情费用',
                  children: [{
                    value: 60001,
                    label: '请客',
                  }, {
                    value: 60002,
                    label: '回礼',
                  }, {
                    value: 60003,
                    label: '孝敬长辈',
                  }]
                }, {
                  value: 70000,
                  label: '休闲娱乐',
                  children: [{
                    value: 70001,
                    label: '聚会',
                  }, {
                    value: 70002,
                    label: '游戏（桌游）',
                  }, {
                    value: 70003,
                    label: '其他娱乐',
                  }]
                }, {
                  value: 80000,
                  label: '保险医疗',
                  children: [{
                    value: 80001,
                    label: '个人保险',
                  }, {
                    value: 80002,
                    label: '医疗费用',
                  }, {
                    value: 80003,
                    label: '其他娱乐',
                  }]
                }, {
                  value: 90000,
                  label: '个人投资',
                  children: [{
                    value: 90001,
                    label: '摄影',
                  }, {
                    value: 90002,
                    label: '书包杂志',
                  }, {
                    value: 90003,
                    label: '个人投资',
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
                    accountType: '1',// 消费账户
                    paymentType: '1',
                    fileList:[],
                }
    },
    drawerForm() {
        return {
                    category:'',
                    tag:'',
                    rule: '',
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
                    pickerOptions: pickerOptions,
                }
    },

}



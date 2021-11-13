// account_type INT COMMENT '消费账户 1.老公钱包 2.老婆钱包 3，爷爷钱包 ',
//     payment_type INT COMMENT '付款类型 1.支付宝 2.微信 3.银行卡 4.现金',
//     customer INT COMMENT '消费对象 1.家庭 2.老公 3.老婆 4.牧 ',
//     tag INT COMMENT '标签 1.日常消费（买菜，沃尔玛） 2.一次性消费（零食，购物衣服） 3.固定消费（水电煤，油费，理发话费）'

var __eunm = {
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
    getTag: function(){
        const obj = this.tag;
        return Object.keys(obj).map(
            (key) => ({label: obj[key], value: Number(key)})
            )
    },
    categoryType: [{
                  value: 10000,
                  label: '食品(吃喝)',
                  children: [{
                    value: 10001,
                    label: '买菜',
                  }, {
                    value: 10002,
                    label: '超市(沃尔玛)',
                  }, {
                    value: 10003,
                    label: '水果',
                  }, {
                    value: 10004,
                    label: '零食',
                  }, {
                    value: 10005,
                    label: '工作餐',
                  }]
                }, {
                  value: 20000,
                  label: '居家生活',
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
                    label: '维修费',
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
                    label: '火车',
                  }, {
                    value: 30005,
                    label: '飞机',
                  }, {
                    value: 30006,
                    label: '停车费',
                  }]
                }
    ],
}
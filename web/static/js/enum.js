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
    customer: {
        1: '家庭',
        2: '老公',
        3: '老婆',
        4: '牧牧'
    },
    tag: {
        1: '日常消费',
        2: '一次性消费',
        3: '固定消费'
    }
}
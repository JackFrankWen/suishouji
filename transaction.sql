CREATE TABLE IF NOT EXISTS `transaction`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL  NOT NULL COMMENT '金额',
    categroy_id INT COMMENT '分类ID 0 未分类',
    description VARCHAR(50) COMMENT '描述',
    account_type INT COMMENT '消费账户 1.老公钱包 2.老婆钱包 ',
    payment_type INT COMMENT '付款类型 1.支付宝 2.微信 3.银行卡 4.现金',
    member INT COMMENT '消费对象 1.家庭 2.老公 3.老婆 4.牧 ',
    create_time DATETIME COMMENT'创建时间',
    tag INT COMMENT '标签 1.必须消费 2.一次性消费 3.固定开销'


) COMMENT = '交易明细';

CREATE TABLE IF NOT EXISTS `transaction`(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    amount DECIMAL  NOT NULL COMMENT '金额',
    category JSON DEFAULT NULL COMMENT '分类',
    description VARCHAR(200) COMMENT '描述',
    account_type INT COMMENT '消费账户 1.老公钱包 2.老婆钱包 ',
    payment_type INT COMMENT '付款类型 1.支付宝 2.微信 3.银行卡 4.现金',
    consumer INT COMMENT '消费对象 0.未分配 1.家庭 2.老公 3.老婆 4.牧 ',
    type INT COMMENT '收支类型 1.收入 2.支出 ',
    create_time DATETIME COMMENT'创建时间',
    tag INT COMMENT '标签 1.日常消费（买菜，沃尔玛） 2.一次性消费（零食，购物衣服） 3.固定消费（水电煤，加油费，理发话费）4.'
-- 日常开销，包括餐饮、交通、烟酒、关系、零食、通讯、日用品、等
--
-- 固定支出，包括健身、居家、电子、水电气、旅游、房租等
--
-- 一次性消费
-- 其他支出，包括医疗、学习、美容、不知道该怎么记的烂账等等。

) COMMENT = '交易明细';

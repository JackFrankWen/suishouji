CREATE TABLE IF NOT EXISTS `transaction`(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    amount DECIMAL  NOT NULL COMMENT '金额',
    categroy_id INT COMMENT '分类ID 0 未分类',
    description VARCHAR(200) COMMENT '描述',
    account_type INT COMMENT '消费账户 1.老公钱包 2.老婆钱包 ',
    payment_type INT COMMENT '付款类型 1.支付宝 2.微信 3.银行卡 4.现金',
    customer INT COMMENT '消费对象 1.家庭 2.老公 3.老婆 4.牧 ',
    create_time DATETIME COMMENT'创建时间',
    tag INT COMMENT '标签 1.日常消费（买菜，沃尔玛） 2.一次性消费（零食，购物衣服） 3.固定消费（水电煤，油费，理发话费）4.'
-- 日常开销，包括餐饮、交通、烟酒、关系、零食、通讯、日用品、娱乐等
--
-- 固定支出，包括健身、居家、电子、水电气、旅游、房租等
--
-- 娱乐支出
-- 其他支出，包括医疗、学习、美容、不知道该怎么记的烂账等等。

) COMMENT = '交易明细';

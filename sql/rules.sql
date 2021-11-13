CREATE TABLE IF NOT EXISTS `match_rules`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    rule VARCHAR(20) COMMENT '名称',
    tag INT COMMENT '标签 1.日常消费（买菜，沃尔玛） 2.一次性消费（零食，购物衣服） 3.固定消费（水电煤，油费，理发话费）',
    consumer INT COMMENT '消费对象 1.家庭 2.老公 3.老婆 4.牧 ',
    category JSON DEFAULT NULL COMMENT '分类'

) COMMENT = '分类';
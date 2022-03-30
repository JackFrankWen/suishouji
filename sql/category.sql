CREATE TABLE IF NOT EXISTS `category`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    level INT COMMENT '0. 根目录 1，一级 2.二级',
    name VARCHAR(20) COMMENT '名称',
    pid INT COMMENT '所属上层类目',
    tag INT COMMENT '标签 1.日常消费（买菜，沃尔玛） 2.一次性消费（零食，购物衣服） 3.固定消费（水电煤，油费，理发话费）',
    status INT COMMENT '标签'

) COMMENT = '分类';
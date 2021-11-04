CREATE TABLE IF NOT EXISTS `category`(
    id INT PRIMARY KEY AUTO_INCREMENT,
    level INT COMMENT '0. 根目录 1，一级 2.二级',
    name VARCHAR(20) COMMENT '名称',
    pid INT COMMENT '所属上层类目',
    status INT COMMENT '标签'

) COMMENT = '分类';
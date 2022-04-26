CREATE TABLE IF NOT EXISTS `assets`(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    amount DECIMAL(15,2)  NOT NULL COMMENT '金额',
    assets_cate_id INT COMMENT '资金种类',
    record_time DATETIME COMMENT '记录时间',
    creation_time  DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    modification_time DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    CONSTRAINT fk_AssetCate FOREIGN KEY (assets_cate_id) REFERENCES assets_cate(id)

) COMMENT = '资产';

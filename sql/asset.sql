CREATE TABLE IF NOT EXISTS `asset
`(
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    amount DECIMAL(15,2)  NOT NULL COMMENT '金额',
    category JSON DEFAULT NULL COMMENT '分类',
    description VARCHAR(200) COMMENT '描述',
    account_type INT COMMENT '账户 1.老公钱包 2.老婆钱包 ',
    risk_rank INT COMMENT '风险等级 0 保本 1.低风险 2.微信 3.银行卡 4.现金',
    creation_time     DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    modification_time DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    record_time DATETIME ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

-- 资产分类                                         变现能力
--  现金及活期存款 （现金、活期存折、信用卡、个人支票等）
--  定期存款，通知类存款 （本外币存单）
--  投资资产 （股票、基金（货币基金，）、外汇、债券、房地产）
--  实物资产 （家居物品、住房、汽车）
--  债权资产 （债权、信托、委托贷款等）
--  保险资产 （社保中各基本保险、其他商业保险等）

) COMMENT = '交易明细';
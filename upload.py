import pandas as pd
from sqlalchemy import create_engine


def to_mysql(dataFrame):
    hostname = "localhost"
    dbname = "bookkeep"
    uname = "root"
    pwd = "root"
    tableName = "transaction"
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(host=hostname, db=dbname, user=uname, pw=pwd))
    dbConnection = engine.connect()
    try:
        frame = dataFrame.to_sql(tableName,
                                 dbConnection,
                                 index=False,
                                 if_exists='append'
                                 );

    except ValueError as vx:

        print(vx)

    except Exception as ex:

        print(ex)

    else:

        print("Table %s created successfully." % tableName)

    finally:

        dbConnection.close()



def read_data():
    newData = pd.read_csv('./data/alipay_record_20211105_1511_1.csv',
                          encoding='gb18030',
                          error_bad_lines=False,
                          skiprows=4)

    newData = pd.DataFrame(newData.values, columns=[
        'transactionNumber',  # 交易号
        'byNumber',  # 商家订单号---
        'create_time',  # 交易创建时间
        'paymentTime',  # 付款时间----
        'updateTime',  # 付款时间----
        'transactionFrom',  # 交易来源地----
        'type',  # 类型----
        'payee',  # 交易对方
        'productName',  # 商品名称
        'amount',  # 金额(元)
        'cost_type',  # 收/支
        'status',  # 交易状态---
        'servicePayment',  # 服务费（元）--
        'reciveMoney',  # 成功退款（元）--
        'description',  # 备注
        'cashStatus',  # 资金状态---
        'unNamed'  # ---
    ]
                           )

    newData["description"] = '支付宝，' + newData["payee"].str.strip() + ',' + newData["productName"]
    # 过滤空
    newData = newData[newData['cost_type'].str.strip().astype(bool)]

    newData = newData.drop(columns=[
        'paymentTime',  # 付款时间----
        'cost_type',  # 付款时间----
        'transactionNumber',  # 付款时间----
        'byNumber',  # 付款时间----
        'updateTime',  # 付款时间----
        'transactionFrom',  # 交易来源地----
        'payee',  # 交易来源地----
        'productName',  # 交易来源地----
        'type',  # 类型----
        'status',  # 交易状态---
        'servicePayment',  # 服务费（元）--
        'reciveMoney',  # 成功退款（元）--
        'cashStatus',  # 资金状态---
        'unNamed'  # ---
    ])


    # 过滤没有金额
    newData = newData[newData['amount'] > 0]
    return newData


def main():
    newData = read_data()
    to_mysql(newData)


if __name__ == '__main__':
    main()

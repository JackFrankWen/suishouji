import pandas as pd
from sqlalchemy import create_engine
pd.set_option('display.expand_frame_repr', False)

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



def read_data(csv):
    data_frame = pd.read_csv(csv,
                          encoding='gb18030',
                          error_bad_lines=False,
                          skiprows=4)

    data_frame = pd.DataFrame(data_frame.values, columns=[
        'transactionNumber',  # 交易号
        'byNumber',  # 商家订单号---
        'create_time',  # 交易创建时间
        'paymentTime',  # 付款时间----
        'updateTime',  # 付款时间----
        'transactionFrom',  # 交易来源地----
        'cost_type',  # 类型----
        'payee',  # 交易对方
        'productName',  # 商品名称
        'amount',  # 金额(元)
        'type',  # 收/支
        'status',  # 交易状态---
        'servicePayment',  # 服务费（元）--
        'reciveMoney',  # 成功退款（元）--
        'description',  # 备注
        'cashStatus',  # 资金状态---
        'unNamed'  # ---
    ])

    data_frame["description"] = data_frame["payee"].str.strip() + ',' + data_frame["productName"].str.strip()
    # 过滤空
    data_frame = data_frame[data_frame['type'].str.strip().astype(bool)]





    # 过滤没有金额
    data_frame = data_frame[data_frame['amount'] > 0]

    data_frame.loc[(data_frame['type'].str.contains("支出")), "flow_type"] = '1'

    data_frame.loc[(data_frame['type'].str.contains("收入")), "flow_type"] = '2'
    # data_frame.loc[(data_frame['type'].str.contains("其他")), "flow_type"] = '3'
    # data_frame = data_frame.drop(data_frame[data_frame.flow_type == "3"].index)

    data_frame = data_frame.drop(data_frame[data_frame['status'].str.contains("交易关闭")].index)
    data_frame = data_frame[data_frame["status"].str.contains("交易关闭") == False]


    data_frame = data_frame[data_frame["type"].str.contains("其他") == False]
    data_frame = data_frame.drop(columns=[
        'paymentTime',  # 付款时间----
        'cost_type',  # 收/支
        'transactionNumber',  # 付款时间----
        'byNumber',  # 付款时间----
        'updateTime',  # 付款时间----
        'transactionFrom',  # 交易来源地----
        'payee',  # 交易来源地----
        'productName',  # 交易来源地----
        'status',  # 交易状态---
        'servicePayment',  # 服务费（元）--
        'reciveMoney',  # 成功退款（元）--
        'cashStatus',  # 资金状态---
        'type',  # 资金状态---
        'unNamed'  # ---
    ])
    return data_frame

def read_data_wetchat(csv):
    data_frame = pd.read_csv(csv,
                          error_bad_lines=False,
                          skiprows=16)

    data_frame = pd.DataFrame(data_frame.values, columns=[
        'create_time',  # 交易时间
        'tran_type',  # 交易类型---
        'transaction_from',  # 交易对方
        'productName',  # 商品名称----
        'type',  # 收/支
        'amount',  # 金额(元)
        'paymentType',  # 支付方式----
        'status',  # 交易状态---
        'product_id',  # 交易id
        'merchant_id',  # 商铺ID
        'description' # 备注
    ])

    data_frame["description"] = data_frame["transaction_from"].str.strip() + ',' + data_frame["productName"].str.strip()

    data_frame = data_frame[data_frame["tran_type"].str.contains("转入零钱通") == False]

    data_frame.loc[(data_frame['type'].str.contains("支出")), "flow_type"] = '1'

    data_frame.loc[(data_frame['type'].str.contains("收入")), "flow_type"] = '2'

    data_frame["amount"] = data_frame["amount"].str.replace('¥', '')

    data_frame = data_frame.drop(columns=[
        'tran_type',  # 交易类型---
        'transaction_from',  # 交易对方
        'productName',  # 商品名称----
        'status',  #
        'type',  #
        'paymentType',  # 支付方式----
        'product_id',  # 交易id
        'merchant_id',  # 商铺ID
    ])
    print(data_frame)

    return data_frame


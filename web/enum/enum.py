from enum import Enum
"""
dff
"""
class Tag(Enum):
    """  tag: {
          1: '日常支出',
          2: '变动支出',
          3: '固定支出'
     	 general_cost = 1, variable_cost = 2, fix_cost = 3;

    """
    GENERAL_COST = 1
    VARIABLE_COST = 2
    FIX_COST = 3

class Account(Enum):
      """  消费账户 1.老公钱包 2.老婆钱包

      """
      HUSBAND = 1
      WIFE = 2

class Consumer(Enum):
   """  '消费对象 0.未分配 1.家庭 2.老公 3.老婆 4.牧 '
       consumer: {
          1: '老公',
          2: '老婆',
          3: '家庭',
          4: '牧牧'
      },
   """
   HUSBAND = 1
   WIFE = 2
   FAMILY = 3
   SON = 4

TagString = {
   'GENERAL_COST': '日常支出',
   'VARIABLE_COST': '变动支出',
   'FIX_COST': '固定支出'
}

AccountString = {
   'HUSBAND': '老公钱包',
   'WIFE': '老婆钱包'
}

ConsumerString = {
   'HUSBAND': '老公',
   'WIFE': '老婆',
   'FAMILY': '家庭',
   'SON': '牧牧',
}


def get_account_name(data):
   """

   :param data:
   :return:
   """
   return AccountString[Account(data).name]

def get_consumer_name(data):
   """

   :param data:
   :return:
   """
   return ConsumerString[Consumer(data).name]

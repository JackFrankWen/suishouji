from enum import Enum

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

TagString = {
   'GENERAL_COST': '日常支出',
   'VARIABLE_COST': '变动支出',
   'FIX_COST': '固定支出'
}
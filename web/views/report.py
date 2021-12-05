#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   report.py.py    
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
'''
from web.config import get_config
from web.api.transaction import get_transaction_by_condition
from flask import Blueprint, render_template, request
import json
import decimal

report_blueprint = Blueprint('report', __name__ ,
                                  static_folder='web/static',
                                  template_folder='web/templates')


@report_blueprint.route("/report")
def transaction():
    config = get_config()
    return render_template('report.html',title=config.TITLE, classes=config.CLASSES)


@report_blueprint.route("/report/month/bill", methods=['POST'])
def month_bill():
    data = request.get_json(force=True)
    list = get_transaction_by_condition(data, False)
    return_val = transform_data(list, data['categoryObj'])
    return {'code': 200, 'data': return_val}

def transform_data(list, categoryObj):

    obj = {}

    for item in list:
        amount = item['amount']
        if item['category']:

            arr = json.loads(item['category'])
            lvl1 = str(arr[0])
            lvl2 = str(arr[1])

            if lvl1 in obj.keys():
                obj[lvl1]['amount'] += amount
            else:
                obj[lvl1] = {
                    'amount': decimal.Decimal(0),
                    'child': {
                    }
                }
                obj[lvl1]['amount'] += amount

        else:
            if '00000' not in obj.keys():
                obj['00000'] = {
                    'amount': decimal.Decimal(0),
                    'child': {
                    }
                }
            obj['00000']['amount'] += amount

    return get_list_amount(obj, categoryObj)

def get_list_amount(obj, categoryObj):
    arr = []
    for item in obj:
        new_obj = obj[item]
        new_obj['value'] = str(new_obj['amount'])
        new_obj['id'] = item
        new_obj['name'] = categoryObj[str(item)]
        arr.append(new_obj)
    return arr


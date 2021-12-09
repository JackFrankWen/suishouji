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
from web.api.my_con import run_mysql, query_mysql, query_one
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


@report_blueprint.route("/report/month/track", methods=['POST'])
def month_track():
    data = request.get_json(force=True)

    list = get_transaction_sum_by_condition(data)
    return_val = get_xAxis(list)
    return {'code': 200, 'data': return_val}

@report_blueprint.route("/report/get/month/amount", methods=['POST'])
def year_sum():
    list = get_transaction_sum_by_condition()
    data = get_xAxis(list)
    return {'code': 200, 'data': data}


def get_xAxis(list):
    array_label = []
    array_val = []

    for item in reversed(list):
        array_label.append(item['month'])
        array_val.append(item['total'])
    return {'label': array_label, 'value': array_val}


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


def get_transaction_sum_by_condition(query={}):
    select_clause = "SELECT  SUM(amount) AS total, MONTHNAME(trans_time) AS month FROM `transaction`"
    group_by = " GROUP BY YEAR(trans_time), MONTH(trans_time)"
    where_clause = ''

    if query.get('trans_time'):
        where_clause = ' WHERE trans_time BETWEEN "{}" AND "{}"'.format(query.get('trans_time')[0], query.get('trans_time')[1])

    if query.get('consumer'):
        if where_clause:
            where_clause += ' AND consumer={}'.format(query.get('consumer')[0])
        else:
            where_clause = ' WHERE consumer={}'.format(query.get('consumer')[0])

    if query.get('category'):
        if where_clause:
            where_clause += ' AND json_contains(`category`, "{}") '.format(query.get('category'))
        else:
            where_clause = ' WHERE json_contains(`category`, "{}") '.format(query.get('category'))
    # if query.get('')
    query_clause = select_clause + where_clause + group_by
    print(query_clause)
    return query_mysql(query_clause, '')
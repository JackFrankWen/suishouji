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
import xlwings as xw
import json
from datetime import datetime

import decimal
import os

report_blueprint = Blueprint('report', __name__,
                             static_folder='web/static',
                             template_folder='web/templates')


@report_blueprint.route("/report")
def transaction():
    config = get_config()
    return render_template('report.html', title=config.TITLE, classes=config.CLASSES)


@report_blueprint.route("/report/month/bill", methods=['POST'])
def month_bill():
    data = request.get_json(force=True)

    list = get_transaction_by_condition(data, False)
    return_val = transform_data(list, data['categoryObj'])
    return {'code': 200, 'data': return_val}


@report_blueprint.route("/report/excel/export", methods=['POST'])
def export_year():
    data = request.get_json(force=True)

    list = get_transaction_category_sum_by_condition(data)
    list = sort_list(list)

    to_excel(data, list)
    return {'code': 200}


def sort_list(list):
    obj = {}
    dictlist = []

    for item in list:
        if item["month"] in obj:
            obj[item["month"]].append(item)
        else:
            obj[item["month"]] = []
    for key, value in obj.items():
        dictlist.append(value)
    return dictlist


def to_excel(data, list):
    wb = xw.Book()
    sheet = wb.sheets['Sheet1']
    set_colum_width(sheet)
    category_index = add_sheel_colum(sheet, data.get("categoryObj"))
    add_month_data(list, category_index, sheet)
    save_and_close(wb)


def set_colum_width(sheet):
    sheet.range('A1').column_width = 17
    sheet.range('B1').column_width = 17


def set_colum_color():
    a = (25, 202, 173)
    b = (140, 199, 181)
    c = (160, 238, 225)
    d = (190, 231, 233)
    f = (190, 237, 199)


def save_and_close(wb):
    cwd = os.getcwd()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    file_name = "\\excel\\{}.xlsx".format(dt_string)
    wb.save(cwd + file_name)
    wb.close()


def add_sheel_colum(sheet, list):
    rowA1 = []
    rowB1 = []
    mergeArr = []
    category_index = {}
    point = 1
    mark = 2
    for index, lvl1 in enumerate(list):
        rowA1.append([lvl1.get("label")])
        for index_2, lvl2 in enumerate(lvl1["children"]):
            if index_2 > 0:
                rowA1.append([''])
            point += 1
            category_index[lvl2["value"]] = point
            rowB1.append([lvl2.get("label")])
        row = 'A{}:A{}'.format(mark, point)
        mark = point + 1
        sheet.range(row).merge()
    sheet.range('A2').value = rowA1
    sheet.range('B2').value = rowB1
    return category_index


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def add_month_data(list, category_index, sheet):
    colnum_id = 3
    for sub_list in list:
        for index, value in enumerate(sub_list):
            colnum_str = colnum_string(colnum_id)
            if index == 0:
                str = colnum_str + "1"
                sheet.range(str).value = [value["month"]]
            if json.loads(value.get('category')):
                category = json.loads(value.get('category'))[1]
                place = category_index[category]
                str = "{}{}".format(colnum_str, place)
                sheet.range(str).value = [value["total"]]
        colnum_id += 1


@report_blueprint.route("/report/month/track", methods=['POST'])
def month_track():
    data = request.get_json(force=True)

    list = get_transaction_sum_by_condition(data)
    return_val = get_xAxis(list)
    return {'code': 200, 'data': return_val}


@report_blueprint.route("/report/get/month/amount", methods=['POST'])
def year_sum():
    data = request.get_json(force=True)
    list = get_transaction_sum_by_condition(data)
    data = get_xAxis(list)
    return {'code': 200, 'data': data}


def get_xAxis(list):
    array_label = []
    array_val = []

    for item in list:
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
    select_clause = "SELECT SUM(amount) AS total, MONTHNAME(trans_time) AS month FROM `transaction`"
    group_by = " GROUP BY YEAR(trans_time), MONTH(trans_time) ORDER BY trans_time ASC"
    where_clause = ' WHERE flow_type=1'

    if query.get('trans_time'):
        where_clause += ' AND trans_time BETWEEN "{}" AND "{}"'.format(query.get('trans_time')[0],
                                                                       query.get('trans_time')[1])

    if query.get('consumer'):
        where_clause += ' AND consumer={}'.format(query.get('consumer'))

    if query.get('accountType'):
        where_clause += ' AND account_type={}'.format(query.get('accountType'))

    if query.get('category'):
        where_clause += ' AND json_contains(`category`, "{}") '.format(query.get('category'))

    query_clause = select_clause + where_clause + group_by

    print(query_clause)
    return query_mysql(query_clause, '')


def get_transaction_category_sum_by_condition(query={}):
    select_clause = "SELECT  SUM(amount) AS total, category,MONTHNAME(trans_time) AS month FROM `transaction`"
    group_by = " GROUP BY YEAR(trans_time), MONTH(trans_time), category ORDER BY trans_time ASC"
    where_clause = ' WHERE flow_type=1'

    if query.get('trans_time'):
        where_clause += ' AND trans_time BETWEEN "{}" AND "{}"'.format(query.get('trans_time')[0],
                                                                       query.get('trans_time')[1])

    if query.get('consumer'):
        where_clause += ' AND consumer={}'.format(query.get('consumer')[0])

    if query.get('category'):
        where_clause += ' AND json_contains(`category`, "{}") '.format(query.get('category'))

    query_clause = select_clause + where_clause + group_by

    return query_mysql(query_clause, '')

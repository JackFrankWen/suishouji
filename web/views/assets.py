"""d"""
from flask import Blueprint, render_template, request
from web.api.my_con import run_mysql,query_mysql
from web.enum.enum import to_dict_consumer,to_dict_risk_rank,\
    to_dict_account_type,get_risk_name
import json
assets_blueprint = Blueprint('assets', __name__ ,
                           static_folder='web/static',
                            static_url_path='/',
                           template_folder='/web/templates')


@assets_blueprint.route("/assets/cate/insert", methods=['POST'])
def assets_cate_insert():
    """
    资产大类
    """
    try:
        data = request.get_json(force=True)
        if data.get('id'):
            assets_cate_update(data)
        else:
            assets_cate_create(data)
    except BaseException as err:
        print(err)
    return {'code': 200}


@assets_blueprint.route("/assets/insert", methods=['POST'])
def assets_insert():
    """
    资产条目
    """
    try:
        data = request.get_json(force=True)

        if data.get('id'):
            assets_update(data)
        else:
            assets_create(data)
    except BaseException as err:
        print(err)
    return {'code': 200}


@assets_blueprint.route("/assets/insert/batch", methods=['POST'])
def assets_insert_batch():
    """
    资产条目
    """
    try:
        data = request.get_json(force=True)

        assets_create_batch(data)
    except BaseException as err:
        print(err)
    return {'code': 200}


@assets_blueprint.route("/assets/echarts/overview/pie", methods=['POST'])
def assets_overview_echart():
    """
    资产条目
    """
    try:
        data = request.get_json(force=True)
        risk = transform_risk(get_risk(data))
        category = transform_category(get_category(data))
    except BaseException as err:
        print(err)
    return {'code': 200,
            'category': category,
            'risk': risk}


def get_risk(data):
    query = f"""
    SELECT  SUM(a.amount) as value,a.record_time, b.* 
    FROM assets as a ,assets_cate as b
    WHERE year(record_time)="{data.get('year')}" and month(record_time)='{data.get('month')}' AND a.assets_cate_id = b.id
    GROUP BY risk_rank
    """
    return query_mysql(query, '')


def get_category(data):
    query = f"""
    SELECT  SUM(a.amount) as value,a.record_time, b.* 
    FROM assets as a ,assets_cate as b
    WHERE year(record_time)="{data.get('year')}" and month(record_time)='{data.get('month')}' AND a.assets_cate_id = b.id
    GROUP BY category
    """
    return query_mysql(query, '')


def transform_category(cate_list):
    obj_cate = {}
    arr_category = []
    for item in cate_list:
        category = json.loads(item.get('category'))[0]
        if obj_cate.get(category):
            obj_cate[category] = obj_cate[category] + item.get('value')
        else:
            obj_cate[category] = item.get('value')

    for key in obj_cate:
        arr_category.append({'name': key,'value': obj_cate[key]})
    return arr_category


def transform_risk(risk_list):
    for item in risk_list:
        item['name'] = get_risk_name(item.get('risk_rank'))

    return risk_list


def assets_create_batch(data):
    """
    表assets创建
    :param data:
    """
    values = f""""""
    for key, value in enumerate(data):
        if key == len(data) - 1:
            values += f"""
             ({value.get('amount')},"{value.get('assets_cate_id')}","{value.get('record_time')}")
             """
        else:
            values += f"""
                    ({value.get('amount')},"{value.get('assets_cate_id')}","{value.get('record_time')}"),
                    """

    query_clause = f"""
       INSERT INTO assets
            (amount, assets_cate_id, record_time)
        VALUES {values}
           """
    run_mysql(query_clause, "")


def assets_create(data):
    """
    表assets创建
    :param data:
    """
    query_clause = f"""
       INSERT INTO assets
            (amount, assets_cate_id, record_time)
        VALUES ({data.get('amount')},
            "{data.get('assets_cate_id')}",
            "{data.get('record_time')}")
           """
    print(query_clause)
    run_mysql(query_clause, "")


@assets_blueprint.route("/assets/cate/get", methods=['POST'])
def get_assets_cate():
    """
    获取接口
    """

    data = request.get_json(force=True)
    return {'data': query_assets_cate(data), 'code': 200}


def query_assets_cate(data):
    """
       获取接口
       """

    query = f"""SELECT * FROM assets_cate
       where account_type = {data.get('account_type')}
       """
    return query_mysql(query, '')


def query_assets(data):
    """
       获取接口
       """

    query = f"""
        SELECT a.id, amount,assets_cate_id, record_time,a.creation_time,a.modification_time,MONTH(record_time) AS month
        FROM assets AS a,assets_cate AS b 
        WHERE b.account_type = {data.get('account_type')} AND b.id = a.assets_cate_id 
        ORDER BY record_time asc
    """
    return query_mysql(query, '')


@assets_blueprint.route("/assets/get", methods=['POST'])
def get_assets():
    """
    获取接口
    """
    data = request.get_json(force=True)
    assets_cate = query_assets_cate(data)
    list_assets = query_assets(data)
    data = transform_data(assets_cate, list_assets)

    return {'data': data, 'code': 200}


def transform_data(assets_cate_list, assets_list):
    for assets_cate in assets_cate_list:
        for assets in assets_list:
            if assets_cate.get('id') == assets.get('assets_cate_id'):
                key = f"""month_{assets.get('month')}"""
                if assets_cate.get(key):
                    assets_cate[key].append(assets)
                else:
                    assets_cate[key] = []
                    assets_cate[key].append(assets)
    return assets_cate_list


@assets_blueprint.route("/assets/enum", methods=['POST'])
def assets_enum():
    """
    枚举
    :return:
    """
    data = to_dict_consumer()
    risk_rank = to_dict_risk_rank()
    account_type = to_dict_account_type()
    dict_data = {
        'consumer': data,
        'risk_rank': risk_rank,
        'account_type': account_type,
    }
    return {
        'code': 200,
        'data': dict_data
    }


def assets_cate_create(data):
    """创建"""
    query_clause = f"""
    INSERT INTO assets_cate
         (description, category, account_type, risk_rank)
    VALUES ("{data.get('description')}",
        "{data.get('category')}",
        {data.get('account_type')},
        {data.get('risk_rank')})
        """
    run_mysql(query_clause, "")


def assets_cate_update(data):
    """ assets_cate更新
    """
    query_clause = f"""
    UPDATE assets_cate
    SET description="{data.get('description')}",
    category="{data.get('category')}",
    account_type={data.get('account_type')},
    risk_rank={data.get('risk_rank')}
    WHERE id = {data.get('id')}
    """
    run_mysql(query_clause, "")


def assets_update(data):
    """更新 assets表更新"""
    query_clause = f"""
    UPDATE assets
    SET amount="{data.get('amount')}"
    WHERE id = {data.get('id')}
    """
    run_mysql(query_clause, "")


@assets_blueprint.route("/assets")
def assets():
    """ D发 """
    return render_template('/dashboard.html')

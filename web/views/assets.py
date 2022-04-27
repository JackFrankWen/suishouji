"""d"""
from flask import Blueprint, render_template, request
from web.api.my_con import run_mysql
from web.enum.enum import to_dict_consumer,to_dict_risk_rank,to_dict_account_type
import json

assets_blueprint = Blueprint('assets', __name__ ,
                           static_folder='web/static',
                            static_url_path='/',
                           template_folder='/web/templates')


@assets_blueprint.route("/assets/cate/insert", methods=['POST'])
def assets_cate_insert():
    """
    获取接口
    """
    try:
        data = request.get_data()
        data = json.loads(data)
        if data.get('id'):
            assets_cate_update(data)
        else:
            assets_cate_create(data)
    except  BaseException as err:
        print(err)
    return {'data': 200}


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
    return {'code': 200,
            'data': dict_data
            }


def assets_cate_create(data):
    """创建"""
    query_clause = f"""
    INSERT INTO assets_cate
         (description, category, account_type, risk_rank)
         VALUES ("{data.get('description')}", "{data.get('category')}",  {data.get('account_type')}, {data.get('risk_rank')})
        """
    print(query_clause)
    run_mysql(query_clause, "")


def assets_cate_update(data):
    """更新"""
    query_clause = f"""
    UPDATE assets_cate
    SET description="{data.get('description')}",
    category="{data.get('category')}",
    account_type={data.get('account_type')},
    risk_rank={data.get('risk_rank')}
    WHERE id = {data.get('id')}
    """
    run_mysql(query_clause, "")


@assets_blueprint.route("/assets")
def assets():
    """ D发 """
    return render_template('/dashboard.html')

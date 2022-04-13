from flask import Blueprint, render_template, request
from web.api.my_con import run_mysql, query_mysql, query_one, update_many
from web.api.upload import read_data, to_mysql, read_data_wetchat
from web.api.transaction import get_transaction_by_condition, \
    get_tag_amount_by_condition, \
    get_account_by_condition, \
    get_consumer_by_condition,\
    get_avg_of_last_quarter_amount,\
    get_avg_of_last_year_month_cost
from web.api.word import create_doc
from datetime import datetime
from dateutil.relativedelta import relativedelta
from web.config import get_config
from flask import Response
import re
import json
import decimal
import copy

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


transaction_blueprint = Blueprint('transaction', __name__ ,
                                  static_folder='web/static',
                                  template_folder='web/templates')


@transaction_blueprint.route("/transaction")
def transaction():
    config = get_config()
    return render_template('transaction.html', title=config.TITLE, classes=config.CLASSES)


@transaction_blueprint.route("/add/rule", methods=['POST'])
def add_rule():
    data = request.get_json(force=True)
    obj = search_rule_by_category_and_tag(data)

    if obj:
        data['rule'] = '{}|{}'.format(obj.get('rule'), data.get('rule'))
        data['id'] = obj.get('id')
        update_rule_by_id(data)
    else:
        insert_rule_table(data)
    return {
        "code": "200",
    }


@transaction_blueprint.route("/rule/get/all", methods=['POST'])
def get_rule():

    list = get_all_rule()
    return {
        "code": "200", "list": list
    }


def update_rule_by_id(data):
    query_clause = 'UPDATE match_rules SET rule = "{}",category = "{}",tag = {} WHERE id = {}'.format(
        data.get('rule'),
        data.get('category'),
        data.get('tag'),
        data.get('id'),
    )


    if (data.get('consumer')):
        query_clause = 'UPDATE match_rules SET rule = "{}",category = "{}",tag = {},consumer={}  WHERE id = {}'.format(
            data.get('rule'),
            data.get('category'),
            data.get('tag'),
            data.get('consumer'),
            data.get('id'),
    )
    return run_mysql(query_clause, '')


def insert_rule_table(data):
    add_employee = "INSERT INTO match_rules "
    feild = "(category, tag, rule) "
    feild_value = 'VALUES ("{}", {}, "{}")'.format(
        data.get('category'),
        data.get('tag'),
        data.get('rule'),
    )


    if (data.get('consumer')):
        feild = "(category, tag, rule, consumer) "
        feild_value = 'VALUES ("{}", {}, "{}", {})'.format(
            data.get('category'),
            data.get('tag'),
            data.get('rule'),
            data.get('consumer'),
        )

    add_employee += feild + feild_value
    return run_mysql(add_employee, '')


def search_rule_by_category_and_tag(data):

    query = 'SELECT * FROM match_rules WHERE JSON_CONTAINS(category, "{}") AND tag = {}'.format(
        data.get('category'),
        data.get('tag')
    )

    return query_one(query, '')


@transaction_blueprint.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file:
            if int(request.form['paymentType']) == 1:
                data = read_data(file)
            else:
                data = read_data_wetchat(file)

            data['account_type'] = request.form['accountType']
            data['payment_type'] = request.form['paymentType']  # 导入长
            data['consumer'] = request.form['consumer']  # 导入长
            data = load_rule_data(data)
            res = to_mysql(data)
            return Response(res.get("msg"),status=res.get("code"))
    return {'code': 200}


def load_rule_data(data):

    ruleData = get_all_rule()
    for row in ruleData:
        if(row.get("consumer")):
            data.loc[data['description'].str.contains('{}'.format(row['rule']), regex=True, case=False), 'consumer'] = row['consumer']

        data.loc[data['description'].str.contains('{}'.format(row['rule']), regex=True, case=False), 'tag'] = row['tag']
        data.loc[data['description'].str.contains('{}'.format(row['rule']), regex=True, case=False), 'category'] = row['category']

    return data


def get_all_rule():

    query = "SELECT * FROM match_rules "
    return query_mysql(query, '')




@transaction_blueprint.route("/transaction/query/category", methods=['POST'])
def query_category():
    data = request.get_json(force=True)
    list = get_transaction_by_condition(data, False)
    return_val = transform_data(list, data['categoryObj'])
    return {'code': 200, 'data': return_val}


def get_date_and_sub_month(str, sub_month):
# TODO
    """
    :return:
    """
    date_time_obj = datetime.fromisoformat(str)
    past_date = date_time_obj - relativedelta(months=sub_month)
    return past_date


def hand_data(data):
    """

    :param data:
    :return:
    """
    new_data = copy.deepcopy(data)
    if 'trans_time' in new_data:
        new_data.get('trans_time')[0] = get_date_and_sub_month(new_data.get('trans_time')[0], 1)
        new_data.get('trans_time')[1] = get_date_and_sub_month(new_data.get('trans_time')[1], 1)

    return new_data


def get_category_list(data):
    """

    :param data:
    :return:
    """
    list = get_transaction_by_condition(data, False)
    category_list = transform_data(list, data['categoryObj'])
    return category_list


def get_category_list_last_month(data):
    """

    :param data:
    :return:
    """
    print('===222====')
    print(data)
    print('=======')
    list_last = get_transaction_by_condition(data, False)

    category_list_last_month = transform_data(list_last, data['categoryObj'])
    return category_list_last_month


@transaction_blueprint.route("/transaction/export/word", methods=['POST'])
def export_word():
    data = request.get_json(force=True)
    last = hand_data(data)

    print('===88888888========')
    print(data)
    print(last)
    print('=====88888888======')
    last_year_month_cost_avg = get_avg_of_last_year_month_cost()
    avg_of_last_quarter_amount = get_avg_of_last_quarter_amount(data)

    doc_data = {
        "category": get_category_list(data),
        "category_last_month": get_category_list_last_month(last),

        "last_year_month_cost_avg": last_year_month_cost_avg,
        "avg_of_last_quarter_amount": avg_of_last_quarter_amount,

        "tag": get_tag_amount_by_condition(data),
        "consumer": get_consumer_by_condition(data),
        "account": get_account_by_condition(data),
    }

    create_doc(doc_data)
    return {'code': 200, 'data': 'sss'}


@transaction_blueprint.route("/transcation/delete", methods=['POST'])
def delete():
    data = request.get_json(force=True)
    delete_by_id(data.get('id'))
    return {'code': 200}


@transaction_blueprint.route("/transcation/createorupdate", methods=['POST'])
def create_or_update():
    data = request.get_json(force=True)
    if (data['action'] == 1):
        insert_transcation(data)
    elif data['action'] == 2:
        update_transcation(data)
    return {'code': 200}

@transaction_blueprint.route("/transaction/batch/update", methods=['POST'])
def batch_update():
    data = request.get_json(force=True)
    batch_update_transcation(data)
    return {'code': 200}


@transaction_blueprint.route("/transaction/batch/delete", methods=['POST'])
def batch_delete():
    data = request.get_json(force=True)
    batch_delete_transaction(data)
    return {'code': 200}


@transaction_blueprint.route("/transaction/query/detail", methods=['POST'])
def query_detail():

    data = request.get_json(force=True)
    list = get_transaction_by_condition(data, True)

    return {
        'code': 200,
        'data': list.get('data'),
        'total': list.get('total'),
        'currentPage': list.get('currentPage'),
        'pageSize': list.get('pageSize'),
    }


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

            if lvl2 in obj[lvl1]['child'].keys():
                obj[lvl1]['child'][lvl2] += amount
            else:
                obj[lvl1]['child'][lvl2] = decimal.Decimal(0)
                obj[lvl1]['child'][lvl2] += amount

        else:
            if '100000' not in obj.keys():
                obj['100000'] = {
                    'amount': decimal.Decimal(0),
                    'child': {
                    }
                }
            obj['100000']['amount'] += amount

    return get_list_amount(obj, categoryObj)


def get_list_amount(obj, categoryObj):
    arr = []
    for item in obj:
        child_arr = []
        new_obj = obj[item]
        new_obj['amount'] = str(new_obj['amount'])
        new_obj['id'] = item
        new_obj['label'] = categoryObj[str(item)]
        if 'child' in new_obj.keys():
            child_obj = new_obj['child']
            for child_item in child_obj:
                child_arr.append({
                    'id': child_item,
                    'label':  categoryObj[str(child_item)],
                    'category':  [int(item), int(child_item)],
                    'amount': str(child_obj[child_item])
                })
            new_obj['child'] = child_arr
        arr.append(new_obj)
    return arr


def insert_transcation(data):
    query_clause = ("INSERT INTO transaction"
                  "("
                    "flow_type,"
                    "amount, "
                    "category, "
                    "description, "
                    "account_type, "
                    "payment_type, "
                    "consumer, "
                    "trans_time, "
                    "tag) "
                  "VALUES ("
                    "{},"
                    "{},"
                    '"{}", '
                    "{}, "
                    "{}, "
                    "{}, "
                    "{},"
                    '"{}", '
                    "{})").format(
        1,
        data.get("amount"),
        data.get("category"),
        data.get("description"),
        data.get("account_type"),
        data.get("payment_type"),
        data.get("consumer"),
        data.get("trans_time"),
        data.get("tag")
    )
    return run_mysql(query_clause, "")


def update_transcation(data):
    # 单个更行
    query_clause = ("UPDATE transaction "
           'SET description = "{}",'
                    'category = "{}",'
                    "payment_type = {},"
                    "amount = {},"
                    "consumer = {},"
                    'trans_time = "{}",'
                    "tag = {},"
                    "account_type = {} "
           "WHERE id = {}").format(
        data['description'],
        data['category'],
        data['payment_type'],
        data['amount'],
        data['consumer'],
        data['trans_time'],
        data['tag'],
        data['account_type'],
        data['id'],
    )
    return run_mysql(query_clause, "")


def batch_delete_transaction(data):

    sql_list = str(tuple([key for key in data['ids']])).replace(',)', ')')
    query_clause = ("DELETE FROM transaction "
                    "WHERE id IN {}").format(sql_list)
    return run_mysql(query_clause, '')


def batch_update_transcation(data):
    sql_list = str(tuple([key for key in data['ids']])).replace(',)', ')')

    query_str = ''

    if data.get('category'):
        query_str = 'category = "{}"'.format(data.get('category'))
    if data.get('accountType'):
        if query_str:
            query_str += ','
        query_str += "account_type = {}".format(data.get('accountType'))
    if data.get('consumer'):
        if query_str:
            query_str += ','
        query_str += "consumer = {}".format(data.get('consumer'))
    if data.get('paymentType'):
        if query_str:
            query_str += ','
        query_str += "payment_type = {}".format(data.get('paymentType'))
    if data.get('tag'):
        if query_str:
            query_str += ','
        query_str += "tag = {}".format(data.get('tag'))

    query_clause = ("UPDATE transaction "
                    "SET {query_str} "
                    "WHERE id IN {sql_list}").format(query_str=query_str, sql_list=sql_list)

    return run_mysql(query_clause, '')


def delete_by_id(query_id):
    query_clause = 'DELETE FROM transaction WHERE id ={}'.format(query_id)
    return run_mysql(query_clause, '')


@transaction_blueprint.route("/transaction/auto/classify", methods=['POST'])
def auto_classify():
    data = request.get_json(force=True)
    list = get_transaction_by_condition(data, False)
    match_list = get_match_rule_list(list)
    msg = update_many(match_list, 'transaction')
    return {'code': 200}



def get_match_rule_list(list):
    ruleList = get_all_rule()
    match_list = []
    for item in list:
        for match_rule in ruleList:
            pattern = re.compile(match_rule.get('rule'))
            if pattern.search(item.get('description')):
                item['category'] = match_rule.get('category')
                item['tag'] = match_rule.get('tag')
                del item['modification_time']
                del item['creation_time']
                if match_rule.get('consumer'):
                    item['consumer'] = match_rule.get('consumer')
                match_list.append(item)
    return match_list
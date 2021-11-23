from flask import Blueprint, render_template, request
from web.api.my_con import run_mysql, query_mysql
from web.api.upload import read_data, to_mysql

import json
import  decimal

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
    return render_template('transaction.html')

@transaction_blueprint.route("/add/rule", methods=['POST'])
def add_rule():
    data = request.get_json(force=True)

    mysql_data = {
        'category':  json.dumps(data['data']['category']),
        'tag': data['data']['tag'],
        'rule': data['data']['rule'],
    }

    insert_rule_table(mysql_data)
    return {
        "code": "200",
    }


def insert_rule_table(data):
    add_employee = ("INSERT INTO match_rules "
                    "(category, tag, rule) "
                    "VALUES (%(category)s, %(tag)s, %(rule)s)")
    return run_mysql(add_employee, data)


@transaction_blueprint.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file:
            data = read_data(file)
            data['account_type'] = request.form['accountType']
            data['payment_type'] = request.form['paymentType']
            data = load_rule_data(data)
            to_mysql(data)
            return 'file uploaded successfully'
    return {'code': 200}


def load_rule_data(data):

    ruleData = get_all_rule()
    for row in ruleData:

        data.loc[data['description'].str.contains(row['rule']), 'tag'] = row['tag']
        data.loc[data['description'].str.contains(row['rule']), 'category'] = row['category']

    return data


def get_all_rule():

    query = "SELECT * FROM match_rules "
    return query_mysql(query, '')


def get_transaction_by_condition(query_con, pagination):

    condition = ''
    if query_con.get('picker'):
        condition = ' WHERE create_time BETWEEN "{}" AND "{}"'.format(query_con.get('picker')[0], query_con.get('picker')[1])
        # query_value = [query_con['picker'][0], query_con['picker'][1]]
    if query_con.get('accountType'):
        if not condition:
            condition = " WHERE account_type = {}".format(query_con.get('accountType'))
        else:
            condition += " AND account_type = {}".format(query_con.get('accountType'))

    if query_con.get('paymentType'):
        if not condition:
            condition = " WHERE payment_type = {}".format(query_con.get('paymentType'))
        else:
            condition += " AND payment_type = {}".format(query_con.get('paymentType'))
    if query_con.get('currentPage'):
        offset = (int(query_con.get('currentPage'))-1) * int(query_con.get('pageSize'))
        condition += " LIMIT {} OFFSET {}".format(query_con.get('pageSize'), offset)

    query_clause = "SELECT SQL_CALC_FOUND_ROWS * FROM transaction"
    query_clause += condition
    return query_mysql(query_clause, '', pagination)



@transaction_blueprint.route("/transaction/query/category", methods=['POST'])
def query_category():
    data = request.get_json(force=True)
    list = get_transaction_by_condition(data,False)
    return_val = transform_data(list, data['category'],  data['categoryObj'])
    return {'code': 200, 'data': return_val}


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


@transaction_blueprint.route("/transaction/query/detail", methods=['POST'])
def query_detail():

    data = request.get_json(force=True)
    list = get_transaction_by_condition(data, True)


    return {
        'code': 200,
        'data': list.get('data'),
        'total': list.get('total'),
        'currentPage': data.get('currentPage'),
        'pageSize': data.get('pageSize'),
    }


def transform_data(list, category, categoryObj):

    obj = {
        '00000': {
            'amount': decimal.Decimal(0)
        },
        '10000': {
            'amount': decimal.Decimal(0),
            'child': {
            }
        }
    }

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
            obj['00000']['amount'] += amount

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
                    "create_time, "
                    "tag) "
                  "VALUES ("
                    "%(flow_type)s,"
                    "%(amount)s, "
                    "%(category)s, "
                    "%(description)s, "
                    "%(account_type)s, "
                    "%(payment_type)s, "
                    "%(consumer)s,"
                    "%(create_time)s, "
                    "%(tag)s)")
    query_value = {
        'amount': data['amount'],
        'flow_type': 1,
        'category': json.dumps(data['category']),
        'description': data['description'],
        'account_type': data['account_type'],
        'payment_type': data['payment_type'],
        'consumer': data['consumer'],
        'create_time': data['create_time'],
        'tag': data['tag']
    }
    return  run_mysql(query_clause, query_value)


def update_transcation(data):
    # 单个更行
    query_clause = ("UPDATE transaction "
           "SET description = %(description)s,"
                    "category = %(category)s,"
                    "payment_type = %(payment_type)s,"
                    "consumer = %(consumer)s,"
                    "create_time = %(create_time)s,"
                    "tag = %(tag)s,"
                    "account_type = %(account_type)s "
           "WHERE id = %(id)s")
    query_value = {
        'id': data['id'],
        'category': json.dumps(data['category']),
        'description': data['description'],
        'account_type': data['account_type'],
        'payment_type': data['payment_type'],
        'consumer': data['consumer'],
        'create_time': data['create_time'],
        'tag': data['tag']
    }
    return run_mysql(query_clause, query_value)


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
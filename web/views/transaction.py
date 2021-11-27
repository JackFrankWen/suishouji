from flask import Blueprint, render_template, request
from web.api.my_con import run_mysql, query_mysql,query_one
from web.api.upload import read_data, to_mysql, read_data_wetchat

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

    obj = search_rule_by_category_and_tag(mysql_data)

    if obj:
        mysql_data['rule'] = '{}|{}'.format( obj.get('rule'), mysql_data.get('rule'))
        mysql_data['id'] = obj.get('id')
        update_rule_by_id(mysql_data)
    else:
        insert_rule_table(mysql_data)
    return {
        "code": "200",
    }

def update_rule_by_id( data):
    query_clause = 'UPDATE match_rules SET rule = "{}",category = "{}",tag = {} WHERE id = {}'.format(
        data.get('rule'),
        data.get('category'),
        data.get('tag'),
        data.get('id'),
    )
    return run_mysql(query_clause, '')

def insert_rule_table(data):
    add_employee = ("INSERT INTO match_rules "
                    "(category, tag, rule) "
                    "VALUES (%(category)s, %(tag)s, %(rule)s)")
    return run_mysql(add_employee, data)


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
                data['account_type'] = request.form['accountType']
                data['payment_type'] = request.form['paymentType'] #导入长
                data = load_rule_data(data)
                to_mysql(data)
            else:
                data = read_data_wetchat(file)
                data['account_type'] = request.form['accountType']
                data['payment_type'] = request.form['paymentType']  # 导入长
                data = load_rule_data(data)
                to_mysql(data)
            return 'file uploaded successfully'
    return {'code': 200}


def load_rule_data(data):

    ruleData = get_all_rule()
    for row in ruleData:

        data.loc[data['description'].str.contains('{}'.format(row['rule']), regex=True, case=False), 'tag'] = row['tag']
        data.loc[data['description'].str.contains('{}'.format(row['rule']), regex=True, case=False), 'category'] = row['category']

    return data


def get_all_rule():

    query = "SELECT * FROM match_rules "
    return query_mysql(query, '')


def get_transaction_by_condition(query_con, pagination):

    condition = ''
    if query_con.get('picker'):
        condition = ' AND create_time BETWEEN "{}" AND "{}"'.format(query_con.get('picker')[0], query_con.get('picker')[1])

    if query_con.get('accountType'):
        condition += " AND account_type = {}".format(query_con.get('accountType'))

    if query_con.get('paymentType'):
        condition += " AND payment_type = {}".format(query_con.get('paymentType'))

    if query_con.get('description'):
        condition += ' AND description LIKE "%{}%"'.format(query_con.get('description'))

    if query_con.get('query_null') == "2":
        condition += ' AND consumer IS NULL'

    if query_con.get('query_null') == "3":
        condition += ' AND category IS NULL'

    if query_con.get('query_null') == "4":
        condition += ' AND tag IS NULL'



    condition += " ORDER BY create_time DESC"

    if query_con.get('currentPage'):
        offset = (int(query_con.get('currentPage'))-1) * int(query_con.get('pageSize'))
        condition += " LIMIT {} OFFSET {}".format(query_con.get('pageSize'), offset)

    query_clause = "SELECT SQL_CALC_FOUND_ROWS * FROM transaction WHERE flow_type=1"
    query_clause += condition
    print(query_clause)
    return query_mysql(query_clause, '', pagination)



@transaction_blueprint.route("/transaction/query/category", methods=['POST'])
def query_category():
    data = request.get_json(force=True)
    list = get_transaction_by_condition(data, False)
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
        data.get("create_time"),
        data.get("tag")
    )
    print(query_clause)
    return  run_mysql(query_clause,"")


def update_transcation(data):
    # 单个更行
    query_clause = ("UPDATE transaction "
           'SET description = "{}",'
                    'category = "{}",'
                    "payment_type = {},"
                    "consumer = {},"
                    'create_time = "{}",'
                    "tag = {},"
                    "account_type = {} "
           "WHERE id = {}").format(
        data['description'],
        data['category'],
        data['payment_type'],
        data['consumer'],
        data['create_time'],
        data['tag'],
        data['account_type'],
        data['id'],
    )
    print(query_clause)
    return run_mysql(query_clause, "")


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
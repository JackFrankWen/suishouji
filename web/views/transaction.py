from flask import Blueprint, render_template, request
from web.api.my_con import run_mysql, query_mysql
from web.api.upload import read_data, to_mysql
import decimal

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
    return 'sssssssssss'

def load_rule_data(data):
    ruleData = get_all_rule()
    for row in ruleData:

        data.loc[data['description'].str.contains(row[1]), 'tag'] = row['tag']
        data.loc[data['description'].str.contains(row[1]), 'category'] = row['category']

    return data


def get_all_rule():
    query = "SELECT * FROM match_rules "
    return query_mysql(query, '')


def get_transaction_by_condition(query_con):

    query_clause = "SELECT * FROM transaction "
    query_value = ''
    condition = ''
    if 'picker' in query_con.keys():
        condition = "WHERE create_time BETWEEN %s AND %s"
        query_value = [query_con['picker'][0], query_con['picker'][1]]
    if 'accountType' in query_con.keys():
        if not condition:
            condition = "WHERE accountType = %s"
            query_value.append(query_con['accountType'])
        else:
            condition += "AND accountType = %s"
            query_value = [query_con['accountType']]

    if 'paymentType' in query_con.keys():
        if not condition:
            condition = "WHERE paymentType = %s"
            query_value.append(query_con['accountType'])
        else:
            condition += "AND paymentType = %s"
            query_value = [query_con['paymentType']]

    query_clause += condition
    return query_mysql(query_clause, tuple(query_value))
    # return query_mysql(query_clause, '')



@transaction_blueprint.route("/transaction/query", methods=['POST'])
def query():
    data = request.get_json(force=True)
    list = get_transaction_by_condition(data)
    return_val = transform_data(list, data['category'])
    return {'code':200, 'data': return_val}

def transform_data(list, category):

    obj = {
        '00000':{
            'amount':decimal.Decimal(0)
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

    return get_list_amount(obj)

def get_list_amount(obj):
    arr = []
    for item in obj:
        child_arr = []
        new_obj = obj[item]
        new_obj['amount'] = str(new_obj['amount'])
        new_obj['value'] = item
        if 'child' in new_obj.keys():
            child_obj = new_obj['child']
            for child_item in child_obj:
                child_arr.append({'value': child_item, 'amount': str(child_obj[child_item])})
            new_obj['child'] = child_arr
        arr.append(new_obj)
    print(arr)
    return arr

from flask import Blueprint, render_template, request
from web.api.my_con import run_mysql, query_mysql
from web.api.upload import read_data, to_mysql

import json

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
        print(request.form['accountType'])
        print(request.form['paymentType'])
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

        data.loc[data['description'].str.contains(row[1]), 'tag'] = row[2]
        data.loc[data['description'].str.contains(row[1]), 'category'] = row[3]

    return data


def get_all_rule():
    query = "SELECT * FROM match_rules "
    return query_mysql(query, '')
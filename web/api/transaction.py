from web.api.my_con import run_mysql, query_mysql, query_one


def get_transaction_by_condition(query_con, pagination):
    condition = ''
    if query_con.get('trans_time'):
        condition = ' AND trans_time BETWEEN "{}" AND "{}"'.format(query_con.get('trans_time')[0],
                                                                   query_con.get('trans_time')[1])

    if query_con.get('accountType'):
        condition += " AND account_type = {}".format(query_con.get('accountType'))

    if query_con.get('consumer'):
        condition += " AND consumer = {}".format(query_con.get('consumer'))

    if query_con.get('paymentType'):
        condition += " AND payment_type = {}".format(query_con.get('paymentType'))

    if query_con.get('description'):
        condition += ' AND description LIKE "%{}%"'.format(query_con.get('description'))

    if query_con.get('category'):
        condition += ' AND json_contains(`category`, "{}") '.format(query_con.get('category'))

    if query_con.get('query_null') == "2":
        condition += ' AND consumer IS NULL'

    if query_con.get('query_null') == "3":
        condition += ' AND category IS NULL'

    if query_con.get('query_null') == "4":
        condition += ' AND tag IS NULL'

    condition += " ORDER BY trans_time DESC"

    if query_con.get('currentPage') and pagination:
        offset = (int(query_con.get('currentPage')) - 1) * int(query_con.get('pageSize'))
        condition += " LIMIT {} OFFSET {}".format(query_con.get('pageSize'), offset)
        query_clause = "SELECT SQL_CALC_FOUND_ROWS * FROM transaction WHERE flow_type=1"
    else:
        query_clause = "SELECT * FROM transaction WHERE flow_type=1"

    query_clause += condition
    return query_mysql(query_clause, '', pagination)


def get_tag_amount_by_condition(query_con):
    if query_con.get('trans_time'):
        condition = ' AND trans_time BETWEEN "{}" AND "{}"'.format(query_con.get('trans_time')[0],
                                                                   query_con.get('trans_time')[1])

    query_clause = "SELECT tag,SUM(amount) as total_amount FROM transaction WHERE flow_type=1"
    group_by = "GROUP BY tag"
    query = query_clause + condition + group_by

    return query_mysql(query, '')
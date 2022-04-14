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
        trans_time = ' AND trans_time BETWEEN "{}" AND "{}"'.format(query_con.get('trans_time')[0],
                                                                   query_con.get('trans_time')[1])

    query_clause = f"""
    WITH transaction_co as
         (
            SELECT SUM(amount) as total FROM `transaction` 
            WHERE flow_type = 1 {trans_time}
        )
    SELECT tag,
        SUM(amount) as total_amount,
        ROUND(SUM(amount)/transaction_co.total*100) as percent 
    FROM transaction,transaction_co
    WHERE flow_type=1 {trans_time}
    GROUP BY tag
    """
    return query_mysql(query_clause, '')


def get_account_by_condition(query_con):
    """

    :param query_con:
    :return:
    """
    if query_con.get('trans_time'):
        trans_time = ' AND trans_time BETWEEN "{}" AND "{}"'.format(query_con.get('trans_time')[0],
                                                                   query_con.get('trans_time')[1])

    query_clause = f"""
    SELECT account_type,SUM(amount) as total_amount 
    FROM transaction 
    WHERE flow_type=1 {trans_time}
    GROUP BY account_type
    """

    return query_mysql(query_clause, '')


def get_consumer_by_condition(query_con):
    """
    get consumer
    :param query_con:
    :return:
    """
    if query_con.get('trans_time'):
        trans_time = ' AND trans_time BETWEEN "{}" AND "{}"'.format(query_con.get('trans_time')[0],
                                                                   query_con.get('trans_time')[1])
    query_clause = f"""
        WITH transaction_co as
         (
            SELECT SUM(amount) as total FROM `transaction` 
            WHERE flow_type = 1 {trans_time}
        )
        SELECT consumer,
            SUM(amount) as total_amount,
            ROUND(SUM(amount)/transaction_co.total*100) as percent 
        FROM transaction, transaction_co
        WHERE flow_type = 1 {trans_time}
        GROUP BY consumer
    """
    return query_mysql(query_clause, '')


def get_avg_of_last_year_amount_total():
    """
    去年消费平均
    :return:
    """
    query_clause = f"""
        SELECT AVG(total) as month_avg 
        FROM
        (
            SELECT DATE_FORMAT(trans_time,'%Y-%m') as time, 
            SUM(amount) as total FROM `transaction` WHERE flow_type = 1 
            GROUP BY month(trans_time), year(trans_time)
        ) tra
    """
    return query_mysql(query_clause, '')


def get_avg_of_last_quarter_amount(data):
    """
    过去四个月平均
    :return:
    """
    if data.get('trans_time'):
        trans_time = data.get('trans_time')[0]

    query_clause = f"""
        SELECT AVG(total) as month_avg 
        FROM
        (
            SELECT DATE_FORMAT(trans_time,'%Y-%m') as time, 
            SUM(amount) as total FROM `transaction` 
            WHERE flow_type = 1 AND trans_time between date_sub("{trans_time}",interval 4 month) and "{trans_time}"
            GROUP BY month(trans_time), year(trans_time)
        ) tra
    """
    return query_mysql(query_clause, '')


def get_avg_of_last_year_month_cost():
    """
    去年每月平均
    :return:
    """
    query_clause = f"""
            SELECT AVG(total) as month_avg
           FROM
               (
                    SELECT DATE_FORMAT(trans_time,'%Y-%m') as time, 
                    SUM(amount) as total,
                    tag
                    FROM `transaction` WHERE flow_type = 1 AND year(trans_time)=year(date_sub(now(),interval 1 year))
                    GROUP BY month(trans_time), year(trans_time)
               ) tra
    """
    return query_mysql(query_clause, '')
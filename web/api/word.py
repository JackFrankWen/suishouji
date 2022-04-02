"""生成 word"""
# import os
import decimal
# from datetime import datetime
from docx import Document
from web.enum.enum import Tag,TagString, get_account_name,get_consumer_name

def create_doc(data):
    """
    :param data:
    :return:
    """
    document = Document()

    document.add_heading('三月 账单', 0)

    section_summary(document, data)

    section_compare(document)


    # cwd = os.getcwd()
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M")
    # file_name = "\\demo\\{}.docx".format(dt_string)
    document.save('demo.docx')

def get_tag_name(data):
    """

    :param data:
    :return:
    """
    return TagString[Tag(data).name]

def section_summary(document, data):
    """

    :param document:
    :param data:
    :return:
    """
    document.add_heading('标题1', level=1)

    paragraph_summary(document, data)

    paragraph_account_type(document, data)

    paragraph_consumer(document, data)

    paragraph_cost_from(document, data)

def paragraph_cost_from(document, data):
    """
    消费来源： 固定消费： 3000元， 变动消费：3300，
    :param document:
    :param data:
    :return:
    """
    detail = "消费来源："
    for item in data['tag']:
        label = get_tag_name(item['tag'])
        cost = item['total_amount']
        detail = detail + f"【{label}】{cost}元，"
    document.add_paragraph(detail)
    document.add_paragraph('')

def paragraph_account_type(document, data):
    """
    钱包支出
    :param document:
    :param data:
    :return:
    """
    detail = "钱包支出："
    for item in data['account']:
        label = get_account_name(item['account_type'])
        cost = item['total_amount']
        detail = detail + f"【{label}】{cost}元，"
    document.add_paragraph(detail)
    document.add_paragraph('')

def paragraph_consumer(document, data):
    """
    成员支出
    :param document:
    :param data:
    :return:
    """
    detail = "成员支出："
    for item in data['consumer']:
        label = get_consumer_name(item['consumer'])
        cost = item['total_amount']
        detail = detail + f"【{label}】{cost}元，"
    document.add_paragraph(detail)
    document.add_paragraph('')

def paragraph_summary(document, data):
    """
    本月总支出 【3333】 元。
    其中包括【食品吃喝】【3331】元，购物消费 【2】元。
    :param document:
    :param data:
    :return:
    """
    detail = "其中包括"
    total = decimal.Decimal(0)
    for item in data['summary']:
        title = item['label']
        cost = item['amount']
        total += decimal.Decimal(item['amount'])
        detail = detail + f"【{title}】{cost}元，"

    document.add_paragraph(f"本月总支出 {total} 元。")
    document.add_paragraph('')
    document.add_paragraph(detail)
    document.add_paragraph('')

def section_compare(document):
    """
    d段落二
    :param document:
    :return:
    """
    document.add_heading('标题2', level=1)
    document.add_paragraph('段落2')

"""生成 word"""
import os
import decimal
from datetime import datetime
from docx import Document
from web.enum.enum import Tag,TagString

def create_doc(data):
    """create doc"""
    document = Document()

    document.add_heading('三月 账单', 0)

    section_summary(document, data)

    section_compare(document)


    cwd = os.getcwd()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    file_name = "\\demo\\{}.docx".format(dt_string)
    document.save('demo.docx')

def get_tag_name(data):
    return TagString[Tag(data).name]

def section_summary(document, data):

    document.add_heading('标题1', level=1)
    paragraph_summary(document, data)
    paragraph_cost_from(document, data)

def paragraph_cost_from(document, data):
    detail = "消费来源："
    for item in data['tag']:
        """消费项目： 固定消费： 3000元， 变动消费：3300，"""
        st = "【{}】{}元，".format(get_tag_name(item['tag']), item['total_amount'])
        detail = detail + st
    document.add_paragraph(detail)
    document.add_paragraph('')

def paragraph_summary(document, data):
    detail = "其中包括"
    amount = decimal.Decimal(0)
    total = "本月总支出 {} 元。".format(amount)
    for item in data['summary']:
        """本月总支出 【3333】 元。其中包括【食品吃喝】【3331】元，购物消费 【2】元。"""
        title = item['label']
        cost = item['amount']
        st = f"【{title}】{cost}元，"
        amount += decimal.Decimal(item['amount'])
        detail = detail + st

    document.add_paragraph(total)
    document.add_paragraph('')
    document.add_paragraph(detail)
    document.add_paragraph('')

def section_compare(document):
    document.add_heading('标题2', level=1)
    document.add_paragraph('段落2')



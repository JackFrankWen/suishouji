# 生成word
from docx import Document
from datetime import datetime
import decimal
import os


def create_doc(data):
    """create doc"""
    document = Document()

    document.add_heading('三月 账单', 0)

    sectionSummry(document, data)

    sectionCompare(document)

    document.add_page_break()

    cwd = os.getcwd()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    file_name = "\\demo\\{}.docx".format(dt_string)
    document.save('demo.docx')

def sectionSummry(document, data):
    document.add_heading('标题1', level=1)
    detail = "其中包括"
    amount = decimal.Decimal(0)
    print(data)
    for item in data['summary']:
        """本月总支出 【3333】 元。其中包括【食品吃喝】【3331】元，购物消费 【2】元。"""
        st = "【{}】 【{}】元，".format(item['label'], item['amount'])
        amount += decimal.Decimal(item['amount'])
        detail = detail + st

    total = "本月总支出 【{}】 元。".format(amount)
    document.add_paragraph(total+detail)
    document.add_paragraph('')
    """钱包支出老公钱包 【2000】元， 老婆钱包【1333】元。"""
    """消费占比： 家庭消费 【1111】元，占比45%。 牧牧消费 【1111】元， 消费元"""

def sectionCompare(document):
    document.add_heading('标题2', level=1)
    document.add_paragraph('段落2')
"""生成 word"""
# import os
import decimal
# from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from web.enum.enum import Tag,TagString, get_account_name,get_consumer_name

def to_decial_if_is_string(data):
    """

    :return:
    """
    return decimal.Decimal(data) if isinstance(data, str) else data


def set_style(document):
    """
    设置字体
    :return:
    """
    document.styles['Normal'].font.name = u'宋体'
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    document.styles['Normal'].font.size = Pt(10.5)
    document.styles['Normal'].font.color.rgb = RGBColor(0, 0, 0)


def create_doc(data):
    """
    :param data:
    :return:
    """
    document = Document()

    set_style(document)

    document.add_heading('三月 账单', 0)

    render_data = paragraph_summary(data)

    section_summary(document, data, render_data)

    document.add_page_break()

    section_compare(document, data, render_data)


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


def section_summary(document, data, render_data):
    """

    :param document:
    :param render_data:
    :param data:
    :return:
    """
    document.add_heading('标题1', level=1)
    render_summary(document, render_data)

    paragraph_account_type(document, data)

    paragraph_consumer(document, data)

    paragraph_cost_from(document, data)


def render_summary(document, render_data):
    """

    :param document:
    :param render_data:
    :return:
    """
    document.add_paragraph(render_data.get("total_txt"))
    document.add_paragraph('')
    document.add_paragraph('分类')
    document.add_paragraph(render_data.get("detail_current_month"))
    document.add_paragraph('')


def paragraph_cost_from(document, data):
    """
    消费来源：
    固定消费： 3000元， 变动消费：3300，
    :param document:
    :param data:
    :return:
    """
    detail = ""
    for item in data['tag']:
        label = get_tag_name(item['tag'])
        cost = item['total_amount']
        percent = item['percent']
        detail = detail + f"【{label}】{cost}元，占比 {percent}%。"
    document.add_paragraph('标签')
    document.add_paragraph(detail)
    document.add_paragraph('')


def paragraph_account_type(document, data):
    """
    钱包支出
    :param document:
    :param data:
    :return:
    """
    detail = ""
    for item in data['account']:
        label = get_account_name(item['account_type'])
        cost = item['total_amount']
        detail = detail + f"【{label}】{cost}元，"
    document.add_paragraph("钱包支出：")
    document.add_paragraph(detail)
    document.add_paragraph('')


def paragraph_consumer(document, data):
    """
    成员支出
    :param document:
    :param data:
    :return:
    """
    detail = ""
    for item in data['consumer']:
        label = get_consumer_name(item['consumer'])
        cost = item['total_amount']
        percent = item['percent']
        detail = detail + f"【{label}】{cost}元，占比 {percent}%。"
    document.add_paragraph("成员支出：")
    document.add_paragraph(detail)
    document.add_paragraph('')


def paragraph_summary(data):
    """
    本月总支出 【3333】 元。
    其中包括【食品吃喝】【3331】元，购物消费 【2】元。
    :param document:
    :param data:
    :return:
    """
    detail = "其中包括"
    compare_detail_cost_txt_more = ""
    compare_detail_cost_txt_less = ""
    total = decimal.Decimal(0)

    category_last_month_obj = data['category_last_month_obj']
    for item in data['category']:
        title = item['label']
        item_id = item['id']
        cost = item['amount']
        total += decimal.Decimal(item['amount'])
        detail = detail + f"【{title}】{cost}元，"
        if category_last_month_obj.get(item_id):
            last_item = category_last_month_obj.get(item_id)

            amount_now = decimal.Decimal(item['amount']) if isinstance(item['amount'], str) else item['amount']
            amount_last = decimal.Decimal(last_item['amount']) if isinstance(last_item['amount'], str) else last_item['amount']

            compare_detail_cost = compare_sentence(amount_now, amount_last)
            if amount_now > amount_last:
                compare_detail_cost_txt_more = compare_detail_cost_txt_more + f"【{title}】对比上月支出{compare_detail_cost}, "
            else:
                compare_detail_cost_txt_less = compare_detail_cost_txt_less + f"【{title}】对比上月支出{compare_detail_cost}, "

    total_txt = f"本月总支出 {total} 元。"

    detail_current_month = detail

    total_last_month = decimal.Decimal(0)

    for item in data['category_last_month']:
        total_last_month += decimal.Decimal(item.get('amount'))

    last_year_month_cost_avg_txt = compare_sentence(total, data.get("last_year_month_cost_avg")[0].get("month_avg"))
    avg_of_last_quarter_amount_txt = compare_sentence(total, data.get("avg_of_last_quarter_amount")[0].get("month_avg"))
    compare_last_month_total = compare_sentence(total, total_last_month)

    compare_last_total_txt = f"总支出对比上月 {compare_last_month_total} ，"
    compare_last_year_month_cost_avg_txt = f" 对比去年每月平均{last_year_month_cost_avg_txt}"
    compare_avg_of_last_quarter_amount_txt = f" 对比上个季度每月平均{avg_of_last_quarter_amount_txt}"


    return {
        'total_txt': total_txt,
        'compare_last_total_txt': compare_last_total_txt,
        'detail_current_month': detail_current_month,
        'compare_detail_cost_txt_more': compare_detail_cost_txt_more,
        'compare_detail_cost_txt_less': compare_detail_cost_txt_less,
        'last_year_month_cost_avg_txt': compare_last_year_month_cost_avg_txt,
        'compare_avg_of_last_quarter_amount_txt': compare_avg_of_last_quarter_amount_txt,
    }


def section_compare(document, data, render_data):
    """
    d段落二
    :param document:
    :return:
    """
    document.add_heading('标题2', level=1)
    render_summary_compare(document, render_data)


def render_summary_compare(document, render_data):
    """

    :param document:
    :param render_data:
    :return:
    """
    para = (render_data.get("compare_last_total_txt")
            + render_data.get("last_year_month_cost_avg_txt")
            + render_data.get("compare_avg_of_last_quarter_amount_txt"))

    document.add_heading("总支出对比", 1)
    document.add_paragraph(para)
    document.add_paragraph('')
    document.add_heading("各项支出对比", 1)
    document.add_paragraph("支出增加")
    document.add_paragraph(render_data.get('compare_detail_cost_txt_more'))
    document.add_paragraph("支出减少")
    document.add_paragraph(render_data.get('compare_detail_cost_txt_less'))
    document.add_paragraph('')


def compare_sentence(cur, old):
    """
    对比
    :param cur:
    :param old:
    :return:
    """
    sentence = ''
    a = cur
    b = old
    if isinstance(a, str):
        a = decimal.Decimal(a)
    if isinstance(b, str):
        b = decimal.Decimal(b)

    cost = round(a - b, 2)
    if cost > 0:
        sentence = f"增加了{cost}元"
    elif cost == 0:
        sentence = "不变"
    else:
        sentence = f"减少了{abs(cost)} 元 "

    return sentence

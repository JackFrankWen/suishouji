"""d"""
from flask import Blueprint, render_template
assets_blueprint = Blueprint('assets', __name__ ,
                           static_folder='web/static',
                            static_url_path='/',
                           template_folder='/web/templates')


@assets_blueprint.route("/assets/demo", methods=['POST'])
def demo1():
    """ D发 """
    return {'code': 200, 'data': 'sss'}


@assets_blueprint.route("/assets")
def assets():
    """ D发 """
    return render_template('/dashboard.html')

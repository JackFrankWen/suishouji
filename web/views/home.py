from flask import Blueprint, render_template

home_blueprint = Blueprint('home', __name__ ,
                           static_folder='web/static',
                           template_folder='web/templates')

@home_blueprint.route("/")
def index():
    """ D发 """
    return render_template('index.html')

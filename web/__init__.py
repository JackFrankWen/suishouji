# 网站模块
"""d"""
from flask import Flask
from web.views.home import home_blueprint
from web.views.transaction import transaction_blueprint
from web.views.report import report_blueprint
from web.views.assets import assets_blueprint


def create_app():
    """d"""
    app = Flask(__name__,
                )
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.register_blueprint(home_blueprint)
    app.register_blueprint(transaction_blueprint)
    app.register_blueprint(report_blueprint)
    app.register_blueprint(assets_blueprint)
    return app

from flask import Flask
from web.views.home import home_blueprint
from web.views.transaction import transaction_blueprint
import os


def create_app():

    app = Flask(__name__,
                )
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.register_blueprint(home_blueprint)
    app.register_blueprint(transaction_blueprint)
    return app

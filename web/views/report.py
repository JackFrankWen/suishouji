#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   report.py.py    
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
'''
from web.config import get_config

from flask import Blueprint, render_template, request
report_blueprint = Blueprint('report', __name__ ,
                                  static_folder='web/static',
                                  template_folder='web/templates')


@report_blueprint.route("/report")
def transaction():
    config = get_config()
    return render_template('report.html',title=config.TITLE, classes=config.CLASSES)

# TODO(libing): think more
# -*- coding:utf-8 -*

"""
主blueprint中定义错误处理程序.
"""

from datetime import datetime

from flask import render_template

from . import main


# 如果使用errorhandler装饰器，那么只有blueprint中的错误才能触发处理程序
# 要想注册应用全局的全局处理程序，必须使用app_errorhandler装饰器
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', current_time=datetime.utcnow()), 500

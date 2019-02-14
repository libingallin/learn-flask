# TODO(libing): think more
# -*- coding:utf-8 -*-

"""
把表单对象移到blueprint中.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    """
    在服务器端,每个Web表单都由一个继承自FlaskForm的类表示.
    这个类定义表单中的一组字段，每个字段都用对象表示.字段对象可附属一个或多个*验证函数*.
    *验证函数*用于验证用户提交的数据是否有效.
    """
    name = StringField("What's ur name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

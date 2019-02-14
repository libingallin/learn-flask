# TODO(libing): think more
# -*- coding:utf-8 -*-

"""
创建主蓝本(blueprint).为保持最大的灵活性，在应用中创建一个子包,用于保存应用的第一个blueprint.

在blueprint中定义的路由和错误处理程序处于休眠转台,直到blueprint注册到应用上之后,它们才真正成为应用的一部分.
使用位于全局作用域中的blueprint时,定义路由和错误处理程序的方法几乎和单脚本应用一样.
"""
from flask import Blueprint

# 创建蓝本
main = Blueprint('main', __name__)

# 导入这两个模块就能把路由和错误处理程序与blueprint联系起来
# *在末尾导入*是为了避免循环导入依赖
from . import views, errors

# TODO(libing): think more
# -*- coding:utf-8 -*-

"""
单元测试
"""

import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """尝试创建一个测试环境，尽量与正常运行应用所需的环境一致."""
        # 使用测试配置创建应用
        self.app = create_app('testing')
        # 激活上下文,确保能在测试中使用current_app,就像普通请求一样
        self.app_context = self.app.app_context()
        self.app_context.push()
        # 创建一个全新的数据库,供测试使用
        self.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

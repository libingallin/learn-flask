# TODO(libing): think more
# -*- coding:utf-8 -*-

"""
Flask应用实例在顶级目录中定义,同时还有一些辅助管理应用的任务.
"""

import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # 创建应用实例
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

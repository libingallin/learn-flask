import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
# 应用使用的数据库URL必须保存到Flask配置对象的SQLALCHEMY_DATABASE_URI中
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/test'
# 在不需要跟踪对象变化时降低内存消耗
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db对象是SQLAlchemy类的实现，表示应用使用的数据库
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)


# 在ORM中，模型一般是一个Python类，类中属性对应于数据库表中的列
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')  # 定义关系

    def __repr__(self):
        """没有强制要求，返回一个具有可读性的string表示模型，供调试和测试时使用."""
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 定义外键

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField("What's ur name?", validators=[DataRequired()])
    submit = SubmitField('Submit')


# 创建并注册一个shell下下文处理器
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


# 应用实例需要知道对每个URL的请求要运行哪些代码，所以保存了URL到函数的映射关系
# 处理URL和函数之间关系的程序称为路由.
@app.route('/', methods=['GET', 'POST'])
def index():
    """这样的处理入站请求的函数称为*视图函数(view func)*，返回值是*响应*，是Browser收到的内容."""
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:   # buzai
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.utcnow()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', current_time=datetime.utcnow()), 500

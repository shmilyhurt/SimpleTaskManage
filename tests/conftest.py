import pytest
from task_app import create_app
from task_app.db import db


@pytest.fixture
def app():
    # 创建测试应用
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/task'

    with app.app_context():
        yield app  # 确保返回 Flask 应用实例


@pytest.fixture
def client(app):
    # 创建测试客户端
    return app.test_client()

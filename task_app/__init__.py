from flask import Flask
from .db import db
from .config import Config
from flask_restx import Api
from .api.v1.task_manage import task_ns


# 创建 Flask-RESTX 的 Api 实例
restx_api = Api(
    title='Simple Task API',
    version='1.0',
    description='A simple Task API',
    doc='/swagger/'  # Swagger UI 的访问路径
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化 SQLAlchemy
    db.init_app(app)

    # 初始化 Flask-RESTX
    restx_api.init_app(app)

    restx_api.add_namespace(task_ns)
    return app

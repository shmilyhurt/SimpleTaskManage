from flask_restx import Namespace, fields

# 创建命名空间
task_ns = Namespace('tasks', path='/api/v1/tasks', description='Task Api')

# 定义数据模型
task_model = task_ns.model('Task', {
    'id': fields.Integer(readOnly=True, description='任务id'),
    'title': fields.String(required=True, description='任务标题'),
    'description': fields.String(description='任务描述'),
    'due_date': fields.Date(required=True, description='截止日期'),
    'priority': fields.Integer(required=True, description='优先级'),
    'is_delete': fields.String(required=True, description='是否删除'),
})
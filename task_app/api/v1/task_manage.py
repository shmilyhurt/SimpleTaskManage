from datetime import datetime

from flask import request

from task_app.db import db
from task_app.models.task import Task
from task_app.resp import HttpResponse, HttpStatus
from task_app.swagger.swagger_task import task_ns, task_model
from flask_restx import Resource


@task_ns.route('/')
class TaskList(Resource):
    """
    任务管理系统获取所有任务列表&增加任务
    """
    @task_ns.doc('list_tasks')
    @task_ns.param('page', 'Page number', type=int, default=1)
    @task_ns.param('per_page', 'Items per page', type=int, default=10)
    @task_ns.param('sort_by', 'Sort by field (e.g., due_date, priority)', type=str, default='id')
    @task_ns.param('order', 'Sort order (asc or desc)', type=str, default='asc')
    def get(self):
        """
        根据分页和排序规则返回任务列表
        默认查询非删的数据
        返回前端需要的列表参数和数据
        """
        # 获取分页参数
        page = request.values.get('page', 1, type=int)
        per_page = request.values.get('per_page', 10, type=int)

        # 获取排序参数
        sort_by = request.values.get('sort_by', 'id', type=str)
        order = request.values.get('order', 'asc', type=str)

        # 验证排序字段
        valid_sort_fields = ['id', 'due_date', 'priority']
        if sort_by not in valid_sort_fields:
            return HttpResponse(code=HttpStatus.NOT_FOUND, data={}, msg='Please check field').to_dict()

        # 构建排序条件
        sort_field = getattr(Task, sort_by)
        if order == 'desc':
            sort_field = sort_field.desc()

        # 查询任务列表
        tasks = Task.query.filter(Task.is_delete == 'f').order_by(sort_field).paginate(page=page, per_page=per_page, error_out=False)
        return HttpResponse(code=HttpStatus.OK, data={
            'tasks': [item.to_dict() for item in tasks.items],
            'page': tasks.page,
            'per_page': tasks.per_page,
            'total': tasks.total,
            'pages': tasks.pages
        }, msg='ok').to_dict()

    @task_ns.doc('create_task')
    def post(self):
        """
        创建新任务
        :return:
        """
        try:
            data = request.values
            new_task = Task(
                title=data.get('title'),
                description=data.get('description'),
                due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
                priority=data.get('priority', 1, type=int)
            )
            db.session.add(new_task)
            db.session.commit()
        except ValueError as e:
            return HttpResponse(code=HttpStatus.FIELD_ERROR, data={}, msg=str(e)).to_dict()
        return HttpResponse(code=HttpStatus.OK, data=new_task.to_dict(), msg='ok').to_dict()


@task_ns.route('/<int:task_id>')
@task_ns.param('task_id', 'The task identifier')
class TaskResource(Resource):
    @task_ns.doc('get_task')
    def get(self, task_id):
        """获取所传id的任务详情"""
        task_obj = Task.query.get(task_id)
        if task_obj is None:
            return HttpResponse(code=HttpStatus.NOT_FOUND, data={}, msg='Not Found').to_dict()
        return HttpResponse(code=HttpStatus.OK, data=task_obj.to_dict(), msg='ok').to_dict()

    @task_ns.doc('update_task')
    @task_ns.expect(task_model)
    def put(self, task_id):
        """根据传入的字段和值进行修改任务字段"""
        task_obj = Task.query.get(task_id)
        if task_obj is None:
            return HttpResponse(code=HttpStatus.NOT_FOUND, data={}, msg='Not Found').to_dict()
        data = request.values
        try:
            # 更新字段
            if 'title' in data:
                task_obj.title = data['title']
            if 'description' in data:
                task_obj.description = data['description']
            if 'due_date' in data:
                task_obj.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            if 'priority' in data:
                task_obj.priority = data.get('priority', 1, type=int)
            if 'is_delete' in data:
                task_obj.is_delete = data['is_delete']
            db.session.commit()
            db.session.flush()
        except ValueError as e:
            return HttpResponse(code=HttpStatus.FIELD_ERROR, data={}, msg=str(e)).to_dict()
        return HttpResponse(code=HttpStatus.OK, data=task_obj.to_dict(), msg='ok').to_dict()

    @task_ns.doc('delete_task')
    @task_ns.response(204, 'Task deleted')
    def delete(self, task_id):
        """根据传入的id删除对应任务 逻辑删除"""
        task_obj = Task.query.get(task_id)
        if task_obj is None:
            return HttpResponse(code=HttpStatus.NOT_FOUND, data={}, msg='Not Found').to_dict()

        task_obj.is_delete = 't'
        db.session.commit()
        return HttpResponse(code=HttpStatus.OK, data={}, msg='ok').to_dict()

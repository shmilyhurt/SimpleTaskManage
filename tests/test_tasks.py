import pytest
from task_app.models.task import Task
from datetime import datetime, timedelta
from .conftest import db


# 测试创建任务
def test_create_task(client):
    # 测试数据
    task_data = {
        "title": "完成项目报告",
        "description": "撰写并提交项目报告",
        "due_date": (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
        "priority": 1
    }

    # 发送请求
    response = client.post('/api/v1/tasks/', data=task_data)

    # 验证响应
    assert response.status_code == 200
    data = response.get_json().get('data')
    assert data['title'] == task_data['title']
    assert data['description'] == task_data['description']
    assert data['due_date'] == task_data['due_date']
    assert data['priority'] == task_data['priority']


# 测试获取任务列表
def test_get_tasks(client):
    # 创建测试任务
    task1 = Task(
        title="任务1",
        description="描述1",
        due_date=datetime.today().date(),
        priority=1
    )
    task2 = Task(
        title="任务2",
        description="描述2",
        due_date=datetime.today().date(),
        priority=2
    )
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()

    # 发送请求
    response = client.get('/api/v1/tasks/?sort_by=id&order=desc')

    # 验证响应
    assert response.status_code == 200
    data = response.get_json().get('data').get('tasks')[:2]
    assert len(data) == 2
    assert data[0]['title'] == "任务2"
    assert data[1]['title'] == "任务1"


# 测试获取单个任务
def test_get_task(client):
    # 创建测试任务
    task = Task(
        title="测试任务",
        description="测试描述",
        due_date=datetime.today().date(),
        priority=1
    )
    db.session.add(task)
    db.session.commit()

    # 发送请求
    response = client.get(f'/api/v1/tasks/{task.id}')

    # 验证响应
    assert response.status_code == 200
    data = response.get_json().get('data')
    assert data['title'] == "测试任务"
    assert data['description'] == "测试描述"


# 测试更新任务
def test_update_task(client):
    # 创建测试任务
    task = Task(
        title="原始标题",
        description="原始描述",
        due_date=datetime.today().date(),
        priority=1
    )
    db.session.add(task)
    db.session.commit()

    # 更新数据
    update_data = {
        "title": "更新后的标题",
        "priority": 3
    }

    # 发送请求
    response = client.put(f'/api/v1/tasks/{task.id}', data=update_data)

    # 验证响应
    assert response.status_code == 200
    data = response.get_json().get('data')
    assert data['title'] == "更新后的标题"
    assert data['priority'] == 3


# 测试删除任务
def test_delete_task(client):
    # 创建测试任务
    task = Task(
        title="待删除任务",
        description="待删除描述",
        due_date=datetime.today().date(),
        priority=1
    )
    db.session.add(task)
    db.session.commit()

    # 发送请求
    response = client.delete(f'/api/v1/tasks/{task.id}')

    # 验证响应
    assert response.status_code == 200

    # 验证任务是否已删除
    deleted_task = Task.query.filter(Task.id == task.id, Task.is_delete == 'f')
    assert deleted_task.count() == 0

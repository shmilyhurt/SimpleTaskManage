# SimpleTaskManage

代码结构:
```
task_app api的主要文档 包括
api的逻辑代码（版本控制）
model的定义 
原生sql 
swagger的引入和设置
 
tests 包括
单元测试代码

其他文件 包括 
项目启动文件
docker相关文件
gunicorn配置文件等
```
代码设计:
```
1.使用orm定义models，设计完成的sql语句
2.使用flask_restx接入swagger,并按照代码规格设计api的接口模式
3.在model中添加字段验证
4.在api中进行正常或者异常处理
5.自定义状态码和响应数据格式
6.api的版本控制
7.完成的单元测试
8.容器化的启动方案
```
如何启动：
```
在开发环境中，可以在命令行使用flask run启动该项目

在正式环境中， 配置gunicorn配置文件&nginx配置文件，完成flask启动配置
使用docker build完整镜像
使用docker-compse 启动容器

因本地环境问题，正式环境的流程只写了配置文件和流程，请您谅解
```
接口文档地址
http://127.0.0.1:5000/swagger/
![image](https://github.com/user-attachments/assets/765fac16-48a6-4820-9024-6867c5d3d009)

```



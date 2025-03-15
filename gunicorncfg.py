# Gunicorn 配置文件

# 绑定地址和端口
bind = "0.0.0.0:5000"

# 工作进程数
workers = 4

# 使用 gevent 工作模式
worker_class = "gevent"

# 每个工作进程的最大并发数（gevent 的协程数）
worker_connections = 1000

# 超时时间（秒）
timeout = 30

# 日志配置
accesslog = "-"  # 访问日志输出到标准输出
errorlog = "-"   # 错误日志输出到标准错误




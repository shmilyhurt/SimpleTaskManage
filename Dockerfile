# 使用官方 Python 3.10 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 使用 Gunicorn 启动 Flask 应用
CMD ["gunicorn", "--config", "gunicorncfg.py", "run:app"]
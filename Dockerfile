
# 使用极其轻量的 Python 3.9 基础镜像
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/python:3.9-slim
WORKDIR /app

# 拷贝代码
COPY app.py /app/

# 简历高光点：使用阿里云镜像源加速依赖拉取，解决国内超时问题
RUN pip install flask -i https://mirrors.aliyun.com/pypi/simple/

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "app.py"]

# 使用极其轻量的 Python 3.9 基础镜像
FROM docker.m.daocloud.io/library/python:3.9-slim
WORKDIR /app

# 🌟 SRE 进阶考点：分离拷贝，利用分层缓存机制！
# 先只拷贝配料表。这样只要 requirements.txt 不变，下次构建就会直接复用缓存，秒级完成打包！
COPY requirements.txt /app/

# 简历高光点：使用阿里云镜像源加速依赖拉取，解决国内超时问题
# 增加 --no-cache-dir 参数：安装完不留本地缓存垃圾，极致压缩镜像体积！
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 依赖装完后，再拷贝经常改动的业务代码
COPY app.py /app/

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "app.py"]

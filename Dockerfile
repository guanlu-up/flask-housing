# 构建镜像; 基于python3.10的系统环境
# docker build -t <ImageName> .

FROM python:3.10-bullseye

# 工作目录，不存在会自动创建
WORKDIR /root/src/app

# apt 更换源
RUN sed -i "s/archive.ubuntu./mirrors.aliyun./g" /etc/apt/sources.list
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN sed -i "s/security.debian.org/mirrors.aliyun.com\/debian-security/g" /etc/apt/sources.list
RUN sed -i "s/httpredir.debian.org/mirrors.aliyun.com\/debian-security/g" /etc/apt/sources.list

# pip 更换源
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com

# 复制文件; COPY <源路径> <目标路径>
COPY requirements.txt .
COPY WebAPI WebAPI/
# 在构建镜像的过程中执行参数
RUN pip install --upgrade pip && pip install --no-cache-dir  -r requirements.txt

# 暴露端口
EXPOSE 8001

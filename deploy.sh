# $(pwd) 表示在项目路径下
# 运行flask镜像服务
docker run -it --rm \
  -v $(pwd):/root/src/app \
  -p 8001:8001 \
  --name flask-homeapp \
  --network app-dev \
  myflaskapp \
  /bin/bash

# 运行mysql镜像服务,将数据映射到本地
docker run -d \
  --name mysql-homeapp \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -v $(pwd)/cachedata/mysql/log:/var/log/mysql \
  -v $(pwd)/cachedata/mysql/data:/var/lib/mysql \
  -v $(pwd)/cachedata/mysql/conf:/etc/mysql/conf.d \
  mysql

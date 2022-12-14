## Dockerfile
```shell
$ pwd
/root/Flask-HomeApp

$ docker build -t flaskhomeapp .
```
---

## migrations
### step:
先将flask实例所在的文件路径绑定到FLASK_APP系统变量中
```shell
export FLASK_APP=/app/app.py
```
```shell
# 初始化迁移文件; 如同 git init
flask db init
# 将模型添加到迁移文件(在项目的数据库结构发生改变时)
flask db migrate
# 迁移文件中的模型映射到数据库中(在数据库中更新结构)
flask db upgrade
```

### be careful:
- 使用 `flask db upgrade` 后, migrate会在当前项目指定的数据库中的alembic_version表里自动更新一条记录
- 这个表中永远是只有一条记录,保存的是最近一次执行migrate后所保留的版本号(可在 project/migrations/versions 中找到)
---

## celery

```shell
# 启动celery服务:
celery -A WebAPI.celerytask.application worker -l info

# -A WebAPI.celerytask.application : 指定celery app所在的文件路径
# worker : 指定工作方式
# -l info : 输出日志, info级别及以上
```
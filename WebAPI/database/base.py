
from sqlalchemy.orm.query import Query
from sqlalchemy import Column

from ..models import session


class BaseDB(object):
    """base class; 数据库查询"""
    _model = None

    def __init__(self, model):
        """
        :param model: 自定义的Model类(继承自db.Model)
        """
        self._model = model
        self.query: Query(model) = self._model.query

    def query_by_id(self, _id: int):
        """ 根据id进行查询
        :return: Model; self._model
        """
        return self.query.get(_id)

    def query_all(self):
        """查询当前表中所有数据"""
        return self.query.all()

    def update(self, _id: int, mapper: dict, **kwargs):
        """ 根据id查询,更新目标条目的字段值
        :param _id: 要查找的数据条目id
        :param mapper: 需要修改的字段名和字段值映射
        :return: tuple: (Model, bool)
        """
        kwargs.update(mapper)
        # 过滤掉不属于Column的实例并且此属性名称没有绑定在self._model中的key
        keymapper = {key: value for key, value in kwargs.items()
                     if isinstance(key, Column) or hasattr(self._model, key)}
        if not keymapper:
            return None, False
        query: Query = self.query.filter_by(id=_id)
        query.update(keymapper, synchronize_session="fetch")
        session.commit()
        return query.first(), True

    def create(self, column_mapper: dict):
        """ 在数据库表中创建条目
        :param column_mapper: 字段名和字段值映射
        :return: Model; self._model
        """
        model = self._model(**column_mapper)
        session.add(model)
        session.commit()
        return model

    def delete(self, _id: int):
        """根据id删除表中的条目"""
        model = self.query_by_id(_id)
        if model is None:
            return False
        session.delete(model)
        session.commit()
        return True

    def order_by(self, *clauses, limit=None):
        """排序并限制输出数量"""
        orderby = self.query.order_by(*clauses)
        if limit is not None:
            return orderby.limit(limit).all()
        return orderby.all()

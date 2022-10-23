from typing import Optional
from datetime import datetime

from ..database.base import BaseDB
from ..models.order import Order


class OrderDB(BaseDB):

    def __init__(self):
        super(OrderDB, self).__init__(Order)
        self._model = Order

    def query_by_vague_date(
            self,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
    ):
        """ 模糊查询,按日期查询相匹配的所有订单;
        只要数据库中的订单日期包含在参数的日期范围中则认为是相匹配.

        default:
         如果start_date 和 end_date为None, 则认为是当天日期
         如果end_date为None, 则认为和start_date是同一日期
         如果start_date为None, 则认为和end_date是同一日期

        :param start_date: 需要查询的起始日期
        :param end_date: 需要查询的结束日期
        :return: Models
        """
        if not start_date and not end_date:
            start_date = end_date = datetime.date(datetime.now())
        elif start_date and not end_date:
            end_date = start_date
        elif not start_date and end_date:
            start_date = end_date

        syntax = self.query.filter(
            self._model.start_time <= end_date,
            self._model.end_date >= start_date
        )
        return syntax.all()

    def query_by_exact_date(
            self,
            start_date: Optional[datetime],
            end_date: Optional[datetime],
    ):
        """ 精确查询,按日期查询相匹配的所有订单;
        :param start_date: 需要查询的订单起始日期
        :param end_date: 需要查询的订单结束日期
        :return: Models
        """

        syntax = self.query.filter(
            self._model.start_time == start_date,
            self._model.end_date == end_date
        )
        return syntax.all()

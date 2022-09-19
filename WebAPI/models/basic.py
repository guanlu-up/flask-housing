from datetime import datetime

import sqlalchemy as alchemy


class RecordTimeModel(object):
    """基础Model; 包含数据的创建日期和更新日期"""

    start_time = alchemy.Column(alchemy.DateTime, default=datetime.now)
    # 当这条记录发生变化时会自动onupdate方法并更新到update_time字段中
    update_time = alchemy.Column(alchemy.DateTime, default=datetime.now, onupdate=datetime.now)

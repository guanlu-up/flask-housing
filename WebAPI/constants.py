class Auth(object):

    # 登录重试次数
    RETRY_TIMES_MAX = 5
    # 当账户错误次数达到阈值时被锁定的时间,单位:秒
    ACCOUNT_LOCKOUT_TIME = (60 * 5)


class Versatile(object):
    # 城区名称信息在redis中保存的时长,单位:秒
    CITY_AREAS_TIME = (60 * 60) * 2


class Houses(object):

    # 返回当前销量最好的房源时limit限制
    HOT_HOUSES_LIMIT = 5
    # 当前销量最好的房源信息在redis中保存的key name
    HOT_HOUSES_SIGN = "CurrentHotHouses"
    # 当前销量最好的房源信息在redis中保存的时间
    HOT_HOUSES_TIME = (60 * 60)

    # 在房源搜索页 每页展示房源的数量
    HOUSES_PER_PAGE = 5

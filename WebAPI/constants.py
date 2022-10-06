class AUTH(object):

    # 登录重试次数
    RETRY_TIMES_MAX = 5
    # 当账户错误次数达到阈值时被锁定的时间,单位:秒
    ACCOUNT_LOCKOUT_TIME = (60 * 5)


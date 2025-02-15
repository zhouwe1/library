from enum import Enum


class NOTIFY(Enum):
    notify_hour = '08'  # 通知发送时间-时
    notify_minute = '00'  # 通知发送时间-分
    notify_expired_in_days = 30  # 距归还时间天数小于 notify_expire_days 时发送通知

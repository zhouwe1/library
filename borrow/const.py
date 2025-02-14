from enum import Enum


class CONFIG(Enum):
    borrow_days = 30  # 借书期限
    notify_time = '08:00'  # 通知发送时间
    notify_expire_days = 7  # 距归还时间天数小于 notify_expire_days 时发送通知

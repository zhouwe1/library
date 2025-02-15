from celery import shared_task
from .models import Borrow


@shared_task
def notify_expired_in_days(days: int):
    borrows = Borrow.expired_in_days(days)
    for b in borrows:
        msg = f'亲爱的读者，您借阅的《{b.book.title}》将于{b.end_time}到期，请尽快归还！'
        print(b.user.phone, msg)
    return 'success'

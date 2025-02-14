from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from book.models import Detail as BookDetail
from .const import CONFIG
# Create your models here.


class Borrow(models.Model):
    book = models.ForeignKey(to="book.Book", related_name="borrows", on_delete=models.PROTECT)
    book_detail = models.ForeignKey(to="book.Detail", related_name="borrows", on_delete=models.PROTECT)
    user = models.ForeignKey(to="user.User", related_name="borrows", on_delete=models.PROTECT)
    start_time = models.DateTimeField(default=now)  # 借书时间
    end_time = models.DateTimeField(db_index=True)  # 到期时间
    returned_time = models.DateTimeField(default=None, db_index=True, null=True)  # 还书时间

    @staticmethod
    def borrowing(detail_uuid, user_id):
        # 借书
        current_time = now()
        detail = BookDetail.objects.filter(uuid=detail_uuid, is_disabled=False, book__is_disabled=False).first()
        if not detail:
            return {'code': 2, 'msg': '图书无效', 'data': {}}
        borrow = Borrow.objects.filter(book_detail=detail, returned_time=None).first()
        if borrow and borrow.user_id == user_id:
            # 图书已被该用户借走
            return {'code': 2, 'msg': '已借阅成功，请勿重复操作', 'data': {
                'start_time': borrow.start_time,
                'end_time': borrow.end_time
            }}
        elif borrow:
            # 图书已被借出
            return {'code': 2, 'msg': '图书无效', 'data': {}}
        end_time = current_time+ timedelta(days=CONFIG.borrow_days.value)
        borrow = Borrow(book=detail.book, book_detail=detail, user_id=user_id, start_time=current_time, end_time=end_time)
        borrow.save()
        return {
            'code': 0,
            'msg': '借书成功',
            'data':{
                'start_time': current_time,
                'end_time': end_time
            }
        }

    @staticmethod
    def returning(detail_uuid):
        # 还书
        borrow = Borrow.objects.filter(book_detail__uuid=detail_uuid, returned_time=None).first()
        if not borrow:
            return {'code': 2, 'msg': '数据异常', 'data': {}}
        borrow.returned_time = now()
        borrow.save()
        return {'code': 0, 'msg': '还书成功', 'data': {}}

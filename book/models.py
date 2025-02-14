from django.db import models
from django.db import transaction
from django.utils.timezone import now
from django.core.paginator import Paginator
from uuid import UUID, uuid3
# Create your models here.


UUID_NAMESPACE = UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
SPACE_UUID = UUID('00000000-0000-0000-0000-000000000000')

class Book(models.Model):
    title = models.CharField(max_length=100)  # 书名
    author = models.CharField(max_length=100)  # 作者
    category = models.CharField(max_length=100)  # 图书分类
    image = models.CharField(max_length=100)  # 封面图
    publish_time = models.CharField(max_length=100)  # 出版时间
    publishing_house = models.CharField(max_length=100)  # 出版社
    isbn = models.CharField(max_length=32)  # 书号
    price = models.CharField(max_length=16)  # 价格
    count = models.IntegerField(default=1)  # 图书数量
    serial = models.CharField(max_length=32, unique=True)  # 馆内编号
    desc = models.TextField(default="")  # 图书简介
    is_disabled = models.BooleanField(default=False)  # 是否有效
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField()

    def to_dict(self):
        return {
            'book_id': self.pk,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'isbn': self.isbn,
            'image': self.image,
            'price': self.price,
            'serial': self.serial,
            'desc': self.desc,
            'publish_time': self.publish_time,
            'publishing_house': self.publishing_house,
            'count': self.count,
            'create_time': self.create_time,
            'update_time': self.update_time,
        }

    @property
    def book_uuid(self):
        """计算图书的UUID，用来生成detail的uuid3"""
        return uuid3(UUID_NAMESPACE, str(self.pk))

    @staticmethod
    def add_book(data: dict):
        current_time = now()
        with transaction.atomic():
            book = Book(
                **data,
                create_time=current_time,
                update_time=current_time,
            )
            book.save()
            book_uuid = book.book_uuid
            # 创建detail记录
            details = []
            for i in range(book.count):
                d = Detail(
                    book=book,
                    uuid=SPACE_UUID,
                    create_time=current_time,
                    update_time=current_time,
                )
                d.save()
                d.uuid = uuid3(book_uuid, str(d.pk))
                d.save()
                details.append(d.uuid)
        result = book.to_dict()
        result['details'] = details
        return result

    def edit_book(self,data: dict):
        for k, v in data.items():
            setattr(self, k, v)
        self.update_time = now()
        self.save()

    def delete_book(self):
        self.update_time = now()
        self.is_disabled = True
        self.save()

    @staticmethod
    def search(params: dict, page: int, per_page: int):
        options = {'is_disabled': False}
        if params.get('title'):
            options['title__icontains'] = params.get('title')
        if params.get('author'):
            options['author__contains'] = params.get('author')
        if params.get('category'):
            options['category'] = params.get('category')
        if params.get('isbn'):
            options['isbn'] = params.get('isbn')
        if params.get('serial'):
            options['serial'] = params.get('serial')

        result = []
        all_books = Book.objects.filter(**options).order_by('id').all()
        paging = Paginator(all_books, per_page)
        current_page = paging.get_page(page)
        for book in current_page:
            result.append(book.to_dict())
        return {
            'list': result,
            'paginate': {
                'item_nums': paging.count,
                'page_nums': paging.num_pages,
            }
        }


class Detail(models.Model):
    book = models.ForeignKey(to="book.Book", related_name="details", on_delete=models.PROTECT)
    uuid = models.UUIDField()
    is_disabled = models.BooleanField(default=False)  # 是否有效
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField()

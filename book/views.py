from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError
import json
from utils import json_response, timer
from .models import Book
from .schemas import BookData
# Create your views here.



@method_decorator(csrf_exempt, name='dispatch')
class BookView(View):

    # 查询
    @timer
    def get(self, request):
        params = request.GET
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        result = Book.search(params, page, per_page)
        return json_response(code=0, data=result)

    # 录入
    @timer
    def post(self, request):
        data = json.loads(request.body)
        try:
            book_data = BookData(**data)
        except ValidationError:
            return json_response(code=1, msg='参数错误', data={})
        book = Book.objects.filter(serial=book_data.serial, is_disabled=False).first()
        if book:
            return json_response(code=2, msg='该图书已存在', data=book.to_dict())
        result = Book.add_book(book_data.model_dump())
        return json_response(code=0, msg='添加成功', data=result)

    # 修改
    @timer
    def put(self, request, book_id):
        data = json.loads(request.body)
        try:
            book_data = BookData(**data)
        except ValidationError as e:
            return json_response(code=1, msg='参数错误', data={})
        book = Book.objects.filter(id=book_id, is_disabled=False).first()
        if not book:
            return json_response(code=2, msg='图书不存在', data={})
        book.edit_book(book_data.model_dump(exclude={'serial', 'count'}))
        return json_response(code=0, msg='修改成功', data=book.to_dict())

    # 删除
    @timer
    def delete(self, request, book_id):
        book = Book.objects.filter(id=book_id, is_disabled=False).first()
        if not book:
            return json_response(code=2, msg='图书不存在', data={})
        book.delete_book()
        return json_response(code=0, msg='删除成功', data={})

from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError
import json
from utils import json_response
from .schemas import BorrowingReq, ReturningReq
from .models import Borrow
# Create your views here.


@csrf_exempt
def borrowing(request):
    data = json.loads(request.body)
    try:
        book_req = BorrowingReq(**data).model_dump()
    except ValidationError:
        return json_response(code=1, msg='参数错误', data={})
    result = Borrow.borrowing(**book_req)
    return json_response(**result)


@csrf_exempt
def returning(request):
    data = json.loads(request.body)
    try:
        book_data = ReturningReq(**data).model_dump()
    except ValidationError:
        return json_response(code=1, msg='参数错误', data={})
    result = Borrow.returning(**book_data)
    return json_response(**result)

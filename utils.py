from django.http import JsonResponse
import time


def json_response(code: int, data: dict, msg: str = ''):
    """统一返回数据格式"""
    return JsonResponse({'code': code, 'msg': msg, 'data': data})


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f'Spend_time:{ time.time() - start_time}')
        return result
    return wrapper

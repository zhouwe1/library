from django.http import JsonResponse


def json_response(code: int, data: dict, msg: str = ''):
    """统一返回数据格式"""
    return JsonResponse({'code': code, 'msg': msg, 'data': data})

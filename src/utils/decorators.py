#coding:utf-8

from functools import wraps
from django.http import HttpResponse
from django.utils import simplejson as json


def render_to_json(**jsonargs):
    """
    Возвращает JSON ответ переданного словаря или списка
    indent - отступ по умолчанию для красивой печати json в консоли

    @render_to_json()
    def my_view(request, arg1, argN):
        ...
        return {'x': range(4)}

    @render_to_json(indent=2)
    def my_view2(request):
        ...
        return [1, 2, 3]

    """
    def outer(f):
        @wraps(f)
        def inner_json(request, *args, **kwargs):
            result = f(request, *args, **kwargs)
            r = HttpResponse(mimetype='application/json')
            if result:
                indent = jsonargs.pop('indent', 4)
                r.write(json.dumps(result, indent=indent, **jsonargs))
            else:
                r.write("{}")
            return r
        return inner_json
    return outer

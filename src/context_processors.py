#coding:utf-8

from django.conf import settings

def brand(request):
    """
    Словарь с простыми данными по компании
    """
    return {
        'company_name': settings.COMPANY_NAME,
    }
#coding:utf-8

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

from utils.conf_inject import inject_app_defaults
inject_app_defaults(__name__)

email_confirm = getattr(settings, 'REGISTER_EMAIL_CONFIRMATION', True)


def reg_success(request):
    """
    Возвращаю словарь который содержит флаг, что регистрация прошла успешно.

    Если используется подтверждение регистрации через почту в словарь входит 
    сообщение, что для завершения регистрации нужно перейти по ссылке в письме.

    Если подтверждение через почту не используется, то словарь 
    содержит ссылку с редиректом на страницу профиля пользователя.

    """
    result = { 'success': True }

    if email_confirm:
        result['_type'] = 'email'
        result['message'] = u'На указанный Вами адрес электронной почты '\
                            u'отправлено письмо с ссылкой для активации аккаунта.'
    else:
        result['_type'] = ''
        result['next'] = request.REQUEST.get(
            REDIRECT_FIELD_NAME, settings.LOGIN_REDIRECT_URL)

    return result


def get_register_backend():
    """
    Возвращаю строковое представление бекенда регистрации

    В зависимости от того включена или нет в настройках 
    регистрация с подтверждением на почту, использую нужный бекенд

    """
    if email_confirm:
        return 'registration.backends.default.DefaultBackend'
    else:
        return 'registration.backends.simple.SimpleBackend'

#coding:utf-8

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import login as auth_login, logout as auth_logout

from registration.forms import (
    RegistrationFormUniqueEmail, AuthenticationForm, RegistrationForm)

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

DISABLED_UNIQUE_EMAIL = getattr(settings, 'DISABLED_UNIQUE_EMAIL', False)


def get_backend(path):
    """
    Return an instance of a registration backend, given the dotted
    Python import path (as a string) to the backend class.

    If the backend cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.
    
    """
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration backend %s: "%s"' % (module, e))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration backend named "%s"' % (module, attr))
    return backend_class()


class BaseRegAuthBackend(object):
    """
    Базовый класс для бекенда регистрации и аутентификации

    """
    def register(self, request, **kwargs):
        raise NotImplementedError

    def activate(self, request, activation_key):
        raise NotImplementedError

    def login(self, request, form):
        """
        Получаю username and password и авторизую пользователя
        """
        auth_login(request, form.get_user())

    def logout(self, request):
        """
        Завершение сессии пользователя
        """
        auth_logout(request)

    def get_register_form_class(self, request):
        """
        Возвращаю класс формы для регистрации пользователя

        RegistrationFormUniqueEmail - уникальный username и email
        RegistrationForm            - уникальный username
        """
        if DISABLED_UNIQUE_EMAIL:
            return RegistrationForm
        else:
            return RegistrationFormUniqueEmail

    def get_login_form_class(self, request):
        """
        Возвращаю класс формы для аутентификации пользователя
        """
        return AuthenticationForm

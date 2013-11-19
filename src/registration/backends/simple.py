#coding:utf-8

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

from registration import signals
from registration.backends import BaseRegAuthBackend


class SimpleBackend(BaseRegAuthBackend):
    """
    Простая регистрация пользователя. 
    Он вводит логин, email и пароль и сразу же входит

    """
    def register(self, request, **kwargs):
        """
        Создаю нового пользователя и сразу авторизую

        """
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        User.objects.create_user(username, email, password)

        new_user = authenticate(username=username, password=password)

        auth_login(request, new_user)

        signals.user_registered.send(
            sender=self.__class__, user=new_user, request=request)

    def activate(self, **kwargs):
        raise NotImplementedError

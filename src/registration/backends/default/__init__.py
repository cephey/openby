#coding:utf-8

from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.forms import RegistrationFormUniqueEmail, AuthenticationForm, RegistrationForm
from registration.models import RegistrationProfile

DISABLED_UNIQUE_EMAIL = getattr(settings, 'DISABLED_UNIQUE_EMAIL', False)


class DefaultBackend(object):
    """
    Бэкенд для регистрации, активации и аутентификации пользователя    
    """

    def register(self, request, **kwargs):
        """
        Получаю username, email address and password и 
        регистрирую нового неактивного пользователя
        """

        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

    def activate(self, request, activation_key):
        """
        Получаю ключ активации, и активирую аккаунт пользователя, 
        которому он принадлежит
        """

        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        if activated_user:
            # логинем пользователя. так как перед login всегда надо
            # делать authentication() который принимает логин и пароль
            # (которого сейчас нет) делаю такую нехорошую штуку...
            activated_user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, activated_user)

            signals.user_activated.send(
                sender=self.__class__, user=activated_user, request=request)

        return activated_user

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
#coding:utf-8

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.forms import RegistrationFormUniqueEmail, AuthenticationForm
from registration.models import RegistrationProfile


class DefaultBackend(object):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.
    
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
        Получаю ключ активации, и активарую аккаунт пользователя, 
        которому он принадлежит
        """

        activated = RegistrationProfile.objects.activate_user(activation_key)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated,
                                        request=request)
        return activated

    def login(self, request, form):
        """
        Получаю username and password и авторизую пользователя
        """
        auth_login(request, form.get_user())

    def get_register_form_class(self, request):
        """
        Возвращаю класс формы для регистрации пользователя
        """
        return RegistrationFormUniqueEmail

    def get_login_form_class(self, request):
        """
        Возвращаю класс формы для аутентификации пользователя
        """
        return AuthenticationForm
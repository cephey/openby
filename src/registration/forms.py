#coding:utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegistrationForm(forms.Form):
    """
    Форма регистрации нового пользователя    
    """
    username = forms.RegexField(
        regex=r'^\w+$', max_length=30,
        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})

    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False))
    
    def clean_username(self):
        """
        Проверка что нет пользователя с аналогичным логином
        """

        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Проверка правильности ввода пароля и подтверждения пароля        
        """

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class AuthenticationForm(forms.Form):
    """
    Форма для аутентификации пользователя
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.username_field = User._meta.get_field(User.USERNAME_FIELD)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    _('Please enter a correct %(username)s and password. '
                        'Note that both fields may be case-sensitive.') % {
                    'username': self.username_field.verbose_name
                    })
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account is inactive.'))
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user(self):
        return self.user_cache


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Подкласс 'RegistrationForm', который следит за уникальностью E-mail    
    """
    def clean_email(self):
        """
        Проверка уникальности поля E-mail        
        """

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

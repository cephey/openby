#coding:utf-8

from django.conf import settings
from django.shortcuts import redirect, resolve_url
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.generic import View, TemplateView
from django.utils.http import is_safe_url

from registration.backends import get_backend
from utils.decorators import render_to_json

REG_SUCCESS = {
    'success': True,
    'message': u'На указанный Вами адрес электронной почты '
                u'отправлено письмо с ссылкой для активации аккаунта.'
}


class ActivateView(View):
    """
    Активация нового аккаунта
    """

    def get(self, request, backend, *args, **kwargs):
        backend = get_backend(backend)
        account = backend.activate(request, **kwargs)

        if account:
            messages.success(request, u'Аккаунт успешно активирован')
        else:
            # ошибка активации
            messages.error(request, u'Ошибка активации')

        return redirect('/')


class RegisterView(TemplateView):
    """
    Регистрация нового пользователя
    """
    template_name='registration_form.html'

    def _add_extra_context(self, request, form, extra_context):
        if extra_context is None:
            extra_context = {}
        context = RequestContext(request)
        for key, value in extra_context.items():
            context[key] = callable(value) and value() or value
        context["form"] = form
        
        return context

    def get(self, request, backend, extra_context=None):
        backend = get_backend(backend)

        form_class = backend.get_register_form_class(request)
        form = form_class(scope_prefix='user')
        context = self._add_extra_context(request, form, extra_context)

        return self.render_to_response(context)

    @render_to_json()
    def post(self, request, backend, extra_context=None):
        backend = get_backend(backend)

        form_class = backend.get_register_form_class(request)
        form = form_class(scope_prefix='user', data=request.POST)

        result = {'success': False, 'errors': []}
        if form.is_valid():
            backend.register(request, **form.cleaned_data)
            result = REG_SUCCESS
        else:
            result['errors'] = form.errors

        return result


class LoginView(TemplateView):
    """
    Аутентификация пользователя
    """
    template_name='login_form.html'

    def _add_extra_context(self, request, form, extra_context):
        if extra_context is None:
            extra_context = {}
        context = RequestContext(request)
        for key, value in extra_context.items():
            context[key] = callable(value) and value() or value
        context["form"] = form
        
        return context

    def get(self, request, backend, extra_context=None):
        backend = get_backend(backend)

        form_class = backend.get_login_form_class(request)
        form = form_class(scope_prefix='user')
        context = self._add_extra_context(request, form, extra_context)

        request.session.set_test_cookie()

        return self.render_to_response(context)

    @render_to_json()
    def post(self, request, backend, extra_context=None):
        backend = get_backend(backend)

        form_class = backend.get_login_form_class(request)
        form = form_class(scope_prefix='user', data=request.POST)

        result = {'success': False, 'errors': []}
        if form.is_valid():
            # Проверка безопасного перенаправления
            redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            backend.login(request, form)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            result = {
                'success': True,
                REDIRECT_FIELD_NAME: redirect_to
            }
        else:
            result['errors'] = form.errors

        return result


class LogoutView(View):
    """
    Завершении сессии пользователя
    """

    def get(self, request, backend, *args, **kwargs):
        backend = get_backend(backend)
        backend.logout(request)

        next_page = None
        if REDIRECT_FIELD_NAME in request.REQUEST:
            next_page = request.REQUEST[REDIRECT_FIELD_NAME]

            # Проверка безопасного перенаправления
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = request.path

        if next_page:
            return redirect(next_page)
        else:
            return redirect('/')

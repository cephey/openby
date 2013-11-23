#coding:utf-8

from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView
from django.views.generic.detail import DetailView

from registration import reg_success
from registration.backends import get_backend

from utils.decorators import render_to_json
from utils.mixins import CacheMixin, LoginRequiredMixin


class ActivateView(TemplateView):
    """
    Активация нового аккаунта

    """
    template_name = 'activation_error.html'

    def get(self, request, backend, *args, **kwargs):
        backend = get_backend(backend)
        account = backend.activate(request, **kwargs)

        if account or request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            # ошибка активации
            context = RequestContext(request)
            return self.render_to_response(context)


class RegisterView(TemplateView):
    """
    Регистрация нового пользователя

    """
    template_name='registration_form.html'

    def add_extra_context(self, request, extra_context):
        if extra_context is None:
            extra_context = {}
        context = RequestContext(request)
        for key, value in extra_context.items():
            context[key] = callable(value) and value() or value

        return context

    def get(self, request, backend, extra_context=None):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            context = self.add_extra_context(request, extra_context)
            return self.render_to_response(context)

    @render_to_json()
    def post(self, request, backend, extra_context=None):
        backend = get_backend(backend)

        form_class = backend.get_register_form_class(request)
        form = form_class(data=request.POST)

        result = {'success': False, 'errors': []}
        if form.is_valid():
            backend.register(request, **form.cleaned_data)
            result = reg_success(request)
        else:
            result['errors'] = form.errors

        return result


class LoginView(TemplateView):
    """
    Аутентификация пользователя

    """
    template_name='login_form.html'

    def add_extra_context(self, request, extra_context):
        if extra_context is None:
            extra_context = {}
        context = RequestContext(request)
        for key, value in extra_context.items():
            context[key] = callable(value) and value() or value

        return context

    def get(self, request, backend, extra_context=None):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            context = self.add_extra_context(request, extra_context)
            request.session.set_test_cookie()

            return self.render_to_response(context)

    @render_to_json()
    def post(self, request, backend, extra_context=None):
        backend = get_backend(backend)

        form_class = backend.get_login_form_class(request)
        form = form_class(data=request.POST)

        result = {'success': False, 'errors': []}
        if form.is_valid():
            backend.login(request, form)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            redirect_to = request.REQUEST.get(
                REDIRECT_FIELD_NAME, settings.LOGIN_REDIRECT_URL)

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

        return redirect(request.META.get('HTTP_REFERER', '/'))


class ProfileView(LoginRequiredMixin, CacheMixin, DetailView):
    """
    Личный кабинет

    """
    model = User
    cache_timeout = 0
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        """
        Возвращаю пользователя

        """
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.request.user.id
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        else:
            raise AttributeError(
                u"В {0} не передан id пользователя".\
                format(self.__class__.__name__))

        try:
            obj = queryset.get()
        except User.ObjectDoesNotExist:
            raise Http404(
                "Не найдено {0} соответствующих запросу".\
                format(queryset.model._meta.verbose_name))

        return obj

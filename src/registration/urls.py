#coding:utf-8

from django.conf.urls import patterns, url
# from django.contrib.auth import views as auth_views

from registration import get_register_backend
from registration.views import (LoginView,
                                LogoutView,
                                ActivateView,
                                RegisterView)


urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(),
        {'backend': get_register_backend()},
        name='auth_login'),

    url(r'^logout/$', LogoutView.as_view(), 
        {'backend': get_register_backend()},
        name='auth_logout'),

    url(r'^register/$', RegisterView.as_view(),
        {'backend': get_register_backend()},
        name='registration_register'),

    url(r'^activate/(?P<activation_key>\w+)/$', ActivateView.as_view(),
        {'backend': 'registration.backends.default.DefaultBackend'},
        name='registration_activate'),

                       # url(r'^password/change/$',
                       #     auth_views.password_change,
                       #     name='auth_password_change'),
                       # url(r'^password/change/done/$',
                       #     auth_views.password_change_done,
                       #     name='auth_password_change_done'),
                       # url(r'^password/reset/$',
                       #     auth_views.password_reset,
                       #     name='auth_password_reset'),
                       # url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                       #     auth_views.password_reset_confirm,
                       #     name='auth_password_reset_confirm'),
                       # url(r'^password/reset/complete/$',
                       #     auth_views.password_reset_complete,
                       #     name='auth_password_reset_complete'),
                       # url(r'^password/reset/done/$',
                       #     auth_views.password_reset_done,
                       #     name='auth_password_reset_done'),
)

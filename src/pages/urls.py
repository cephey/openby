# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page


urlpatterns = patterns('',
    url(r'^$', cache_page(60 * 10)(TemplateView.as_view(template_name='index.html')), name="index"),
)
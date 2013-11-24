#coding:utf-8

import sys


def inject_app_defaults(application):
    """
    Вставляю настройки модуля в приложение

    """
    try:
        __import__('%s.settings' % application)

        _app_settings = sys.modules['%s.settings' % application]
        _def_settings = sys.modules['django.conf.global_settings']
        _settings = sys.modules['django.conf'].settings

        for _k in dir(_app_settings):
            if _k.isupper():
                setattr(_def_settings, _k, getattr(_app_settings, _k))

                if not hasattr(_settings, _k):
                    setattr(_settings, _k, getattr(_app_settings, _k))

    except ImportError:
        pass

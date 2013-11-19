#coding:utf-8

import datetime
import hashlib
import random
import re

from django.conf import settings
from django.db import models
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now


SHA1_RE = re.compile('^[a-f0-9]{40}$')
ACCOUNT_ACTIVATION_DAYS = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2)


class RegistrationManager(models.Manager):
    """
    Менеджер для модели ``RegistrationProfile``

    Здесь определены методы для создания учетной записи, 
    активации(в том числе по e-mail) и для очисти аккаунтов 
    в случае когда истекло время активации

    """
    def activate_user(self, activation_key):
        """
        Активация пользователя по ключу

        Если ключ существует и не протух,возвращаю активированного пользователя
        Если ключ существует, но пользователь уже активный, возвращаю ``False``
        Если ключ не существует или протух, возвращаю ``False``

        Для предотвращения реактивации, если админ его деактивировал, 
        ключ сбрасывается в константу ``RegistrationProfile.ACTIVATED`` 
        после успешной активации.

        """
        # проверяю что ключ соответствует структуре SHA1, 
        # а иначе не имеет смысла его искать в базе
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user
        return False
    
    def create_inactive_user(self, username, email, password,
                             site, send_email=True):
        """
        Создаю нового неактивного пользователя, генерирую 
        ``RegistrationProfile``, отправляю ему на почту ключ активацииand 
        и возвращаю нового пользователя

        Для отключения отправки ключа на почту передать``send_email=False``
        
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        registration_profile = self.create_profile(new_user)

        if send_email:
            registration_profile.send_activation_email(site)

        return new_user
    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile(self, user):
        """
        Создание ``RegistrationProfile`` для переданного ``User``
        Возвращаю ``RegistrationProfile``

        Ключ активации будет SHA1 на основе username и соли

        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt+username).hexdigest()

        return self.create(user=user, activation_key=activation_key)
        
    def delete_expired_users(self):
        """
        Удалить просроченные ``RegistrationProfile`` 
        и связанный с ним ``User``
        
        """
        for profile in self.all():
            try:
                if profile.activation_key_expired():
                    user = profile.user
                    if not user.is_active:
                        user.delete()
                        profile.delete()
            except User.DoesNotExist:
                profile.delete()

class RegistrationProfile(models.Model):
    """
    Простой профиль пользователя для разширения модели ``User``

    Хранит в себе ключ активации
    
    """
    ACTIVATED = u"ALREADY_ACTIVATED"
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    
    objects = RegistrationManager()
    
    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user
    
    def activation_key_expired(self):
        """
        Определяет, является ли ключ активации действующим

        Он протухает в 2-х случаях:
        
        1. Если пользователь уже активировал ключ, 
           он устанавливается в ``ACTIVATED``. Повторная 
           активация не допускается, поэтому возвращается ``True``

        2. В противном случае, если прошло времени больше чем указано 
        в ``ACCOUNT_ACTIVATION_DAYS`` то возвращает ``True``
        
        """
        expiration_date = datetime.timedelta(days=ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime_now())
    activation_key_expired.boolean = True

    def send_activation_email(self, site):
        """
        Отправка письма пользователю с ключом активации
        """

        ctx_dict = {
            'activation_key': self.activation_key,
            'expiration_days': ACCOUNT_ACTIVATION_DAYS,
            'site': site}

        subject = render_to_string('activation_email_subject.txt', ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('activation_email.txt', ctx_dict)
        
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

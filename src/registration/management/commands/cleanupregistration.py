#coding:utf-8

from django.core.management.base import NoArgsCommand

from registration.models import RegistrationProfile


class Command(NoArgsCommand):
    help = u"Удаление из базы пользователей с протухшим ключом активации"

    def handle_noargs(self, **options):
        RegistrationProfile.objects.delete_expired_users()

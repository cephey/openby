openby
======

Инструкция по установке
-----------------------

**Установка Redis**::

  sudo apt-get install redis-server

Открываем файл::

  sudo vim /etc/redis/redis.conf

Комментируем::

  #port 6379
  #bind 127.0.0.1

Расскоментируем::

  unixsocket /var/run/redis/redis.sock
  unixsocketperm 777

Перезапускаем redis::

  sudo service redis-server restart

**Установка виртуального окружения**::

  pip install -r requirements.txt

**Инициализация проекта**::

  ./manage.py syncdb

**Настройки**::

После регистрации пользователю высылается письмо для подтверждения регистрации. По умолчанию оно активно в течении 2 дней. Чтобы это переопределить нужно добавить в registration/settings.py::

  ACCOUNT_ACTIVATION_DAYS = 5

По умолчанию для регистрации используется форма которая проверяет уникальность username и email. Если нужно только проверка уникальности username то необходимо добавить в registration/settings.py::

  DISABLED_UNIQUE_EMAIL = True

По умолчанию регистрация идет через подтверждение по электронной почте. Чтобы это отключить необходимо добавить в registration/settings.py::

  REGISTER_EMAIL_CONFIRMATION = False
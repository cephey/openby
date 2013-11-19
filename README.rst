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

**Настройки settings.py**::

После аутентификации пользователь перенапрявляется на страницу указанную в параметре 'next'. Если параметра нет то по умолчанию идет редирект в личный кабинет по адресу '/accounts/profile/'. Чтобы это переопределить нужно добавить в settings.py::

  LOGIN_REDIRECT_URL = '/path/to/profile/'

После регистрации пользователю высылается письмо для подтверждения регистрации. По умолчанию оно активно в течении 2 дней. Чтобы это переопределить нужно добавить в settings.py::

  ACCOUNT_ACTIVATION_DAYS = 5

По умолчанию для регистрации используется форма которая проверяет уникальность username и email. Если нужно только проверка уникальности username то необходимо добавить в settings.py::

  DISABLED_UNIQUE_EMAIL = True

По умолчанию регистрация идет через подтверждение по электронной почте. Чтобы это отключить необходимо добавить в settings.py::

  REGISTER_EMAIL_CONFIRMATION = False
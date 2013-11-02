openby
======

Инструкция по установке
-----------------------

Установка Redis::

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

Установка виртуального окружения::

  pip install -r requirements.txt
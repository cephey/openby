openby
======

template for other site
-----------------------

Инструкция по установке
-----------------------

1 Установка Redis:
    sudo apt-get install redis-server
    sudo vim /etc/redis/redis.conf
        Комментируем:
            #port 6379
            #bind 127.0.0.1
        Расскоментируем:
            unixsocket /var/run/redis/redis.sock
            unixsocketperm 777
    sudo service redis-server restart

2 pip install -r requirements.txt

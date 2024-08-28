## Introduction
This project, 0x02-Redis Basic, demonstrates the fundamentals of using Redis, an open-source in-memory data structure store. Redis is commonly used as a database, cache, and message broker. The project covers basic operations, data storage, and retrieval using Redis.


### Resources
**Read or watch:**

* [Redis Crash Course Tutorial](https://intranet.alxswe.com/rltoken/hJVo3XwMMFFoApyX8zPXvA)
* [Redis commands](https://intranet.alxswe.com/rltoken/oauvbRmxM12SxvimzqhrOg)
* [Redis python client](https://intranet.alxswe.com/rltoken/imfgFhAZPlg7YMZ_tHvFZw)
* [How to Use Redis With Python](https://intranet.alxswe.com/rltoken/7SluvFvgckwVgsvrfOf1CQ)

### Learning Objectives
* Learn how to use redis for basic operations
* Learn how to use redis as a simple cache

### Install Redis on Ubuntu 18.04
$ sudo apt-get -y install redis-server
$ pip3 install redis
$ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf

### Use Redis in a container
Redis server is stopped by default - when you are starting a container, you should start it with: service redis-server start

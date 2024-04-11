# Монорепа команды мисис прогрев градиентов в олимпиаде НТО студтрек КЗ и ЦС

В этом репозитории хранится полное решение команды мисис прогрев градиентов

Рассмотрим по папкам!

#### Main backend (папка app)

Это самый главный сервис, который хранит в себе внешнюю API для взаимодействия [(ссылка на деплой)](http://158.160.138.228:8000/docs#/). Он же хостит телеграм бота, взаимодействует с Redis и Postgres. В нем есть две API ручки, требуемые в изначальном ТЗ. [Ссылка на бота](https://t.me/free_anonymous_vpn_bot). Документация API находится в SwaggerUI

#### ML Service (папка ml_api)

ML сервис, который крутится в датасфере. Имеет несколько роутов, которые должны быть скрыты от интернета

#### Frontend (папка frontend)

Frontend на Streamlit, смотрящий в интернет. [Ссылка на деплой](http://158.160.138.228:8080/)


**Как запустить:**

```
$ cp .env.example .env
$ cp .postgres.env.example .postgres.env
$ # заполнить эти .env файлы
$ docker compose up -d --build
```

*Это не запустит ML сервис, он крутится в датасфере*

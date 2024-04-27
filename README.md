# cheque_bot

### config.py 
- Заменить значение BROWSER, con, admin_id, TOKEN на свои
- При работе на windows использовать BROWSER="chrome", на linux использовать значение "firefox"
### Запуск
1. Подготовка бд mysql
```
create database cheque_bot;

create table if not exists cheques
(
    id          bigint auto_increment,
    user_id     int          null,
    cheque_json text         null,
    qr_url      varchar(500) null,
    verified    tinyint(1)   null,
    constraint cheques_pk
        unique (id)
);

create table if not exists users_data
(
    user_id  varchar(255) null,
    username varchar(255) null
);


```
```
pip install -r requirements.txt
```
Файл для запуска - main_a2.py `python main_a2.py` 
# Тестовое задание
> Примечание
- Я пока только начал изучать JS и не совсем понял, как передать параметр в JS код, но я постарался сделать аналогично все на бекенде.
Буду благодарен, если посмотрите мою реализиацию
- Знаю, что файл .env не надо загружать в git и в docker, но решил так сделать, чтобы проще проверять задание вам

## Задача: 
Реализовать Django + Stripe API бэкенд 

## Варианты установки:

1. С помощью Docker
2. В ручную

### 1 вариант

1. У вас должен быть установлен Docker на компьютере( https://www.docker.com/ )
2. `git clone https://github.com/romaha57/test_task_payment.git`
3. `cd payment_system`
4. `docker build -t app_payment .`
5. `docker run -d -p 8000:8000 app_payment`


### 2 вариант

1. `git clone https://github.com/romaha57/test_task_payment.git`
2. `cd payment_system`
3. `pip install -r requirements.txt`
4. `python manage.py makemigrations`
5. `python manage.py migrate`
6. `python manage.py loaddata user.json`
7. `python manage.py loaddata item.json`
8. `python manage.py loaddata order.json`
9. `python manage.py loaddata tax.json`
10. `python manage.py loaddata discount.json`


## Endpoints's

Просмотр товара:
> localhost:8000/item/{item_id}  -  доступные id = 1, 2, 3

Просмотр заказа пользователя:
> localhost:8000/order/{username}  -  доступный username = admin


## Возможности приложения

- Просмотр товара/заказа
- Создание товара/заказа(через админку)
- Оплата товара/заказа
- Возможность установить скидку на товар/заказ(через админку)
- Возможность установить налог на товар/заказ(через админку)


## Выполненные бонусные задания:
- Docker
- Environment variables
- Просмотр моделей в Django Admin
- Модель Order(заказ пользователя)
- Модель Tax(налоги и вычеты)
- Модель Discount(скидки)

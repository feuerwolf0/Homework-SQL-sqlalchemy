import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import os
import random
import datetime

from models import *

# ------- Конфигурация подключения к БД -------
NAME_DB = 'test'
HOST_DB = 'localhost:5432'
LOGIN_DB = os.getenv('login_db')
PSW_DB = os.getenv('password_db')
# ---------------------------------------------

# Функция для заполнения таблицы данными
def fill_database():
    # Функция для заполнения таблицы данными
    # Наполняю Publisher
    authors = ['Пушкин', 'Братья Стругацкие', 'Толстой', 'Чехов']
    for a in authors:
        session.add(Publisher(name=a))
    session.commit()

    # Наполняю Book
    books = {"Капитанская дочка": 1, 'Руслан и Людмила':1, 'Евгений Онегин':1, "Пиковая дама":1, \
            'Пикник на обочине':2, 'Трудно быть богом': 2, 'Обитаемый остров':2, 'Отель «У погибшего альпиниста»':2,\
                'Война и мир':3, 'Анна Каренина':3, 'Мышь-девочка':3, 'Холстомер':3,\
                    'В ссылке':4, 'Палата № 6': 4, 'Неприятность': 4, 'Дом с мезонином':4}
    for a,b in books.items():
        session.add(Book(title=a, id_publisher=b))
    session.commit()

    # Наполняю Shop
    shops = ['Буквоед', 'Лабиринт', 'Книжный дом']
    for a in shops:
        session.add(Shop(name=a))
    session.commit()

    # Наполняю Stock, использую случайное значени для Count
    for id in range(1,17):
        for shop in range(1,4):
            session.add(Stock(id_book=id, id_shop=shop,count=random.randint(10,80)))
    session.commit()

    # Наполняю Sale
    # Использую случайные цены, даты, число покупок
    for i in range(200):
        session.add(Sale(price=random.randint(400,1000), date_sale=datetime.date(random.randint(2021,2022), random.randint(1,12), random.randint(1,28)), id_stock=random.randint(1,48), count=random.randint(1,10)))
    session.commit()


# ------- Подключение к БД -------
DSN = f'postgresql://{LOGIN_DB}:{PSW_DB}@{HOST_DB}/{NAME_DB}'
engine = sq.create_engine(DSN)

# Удаляю ранее созданные таблицы с данными
# delete_tables(engine)

# Создаю таблицы из models.py
create_tables(engine)

# Создаю сессию
Session = sessionmaker(bind=engine)
session = Session()

# Заполняю базу данных (Только для 1 запуска)
fill_database()

# Получаю список авторов из таблицы Publisher
authors = []
for a in session.query(Publisher.name).all(): authors.append(*a)

# Запрашиваю для какого автора вывести информацию
request_author = ''
while request_author not in authors:
    request_author = input(f'Введите имя автора\nВарианты: {authors}: ')

# Формирую и делаю запрос в БД
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Publisher).\
        join(Stock).\
        join(Shop).\
        join(Sale).\
        filter(Publisher.name == request_author).\
        order_by(Sale.date_sale.desc()).all()

# Вывод результатов
print("{:<20}| {:<15}| {:<6}| {}".format('Название', 'Магазин', 'Цена', 'Дата'))
print('-'*50)
for title, shop, price, date in query:
    print("{:<20}| {:<15}| {:<6}| {}".format(title, shop, price, date))

# Закрываю сессию
session.close()
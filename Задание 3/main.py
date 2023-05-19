import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import os
import json

from models import *

# ------- Конфигурация подключения к БД -------
NAME_DB = 'test'
HOST_DB = 'localhost:5432'
LOGIN_DB = os.getenv('login_db')
PSW_DB = os.getenv('password_db')
# ---------------------------------------------

# ------- Подключение к БД -------
DSN = f'postgresql://{LOGIN_DB}:{PSW_DB}@{HOST_DB}/{NAME_DB}'
engine = sq.create_engine(DSN)

# Удаляю ранее созданные таблицы с данными
delete_tables(engine)

# Создаю таблицы из models.py
create_tables(engine)

# Создаю сессию
Session = sessionmaker(bind=engine)
session = Session()

# Открываю файл json
with open('test_data.json', 'r') as json_file:
    data = json.load(json_file)


for row in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale
    }[row.get('model')]
    session.add(model(id = row.get('pk'),**row.get('fields')))
session.commit()

session.close()
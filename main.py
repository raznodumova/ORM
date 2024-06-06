import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Shop, Publisher, Book, Sale, Stock
import json

login = 'postgres'
password = '5728821q'
localhost = 5432
database = 'HWDB2'


DSN = f'postgresql://{login}:{password}@localhost:{localhost}/{database}'
engine = sqlalchemy.create_engine(DSN)#создание движка для подключения к бд


create_tables(engine)

Session = sessionmaker(bind=engine)#создание сессии
session = Session()

with open('tests_data.json', 'rt') as f:
    data = json.load(f)

for item in data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale
    }[item.get('model')]
    session.add(model(id=item.get('pk'), **item.get('fields')))
    session.commit()


def get_publisher(name=input('Введите имя или id автора: ')):
    search = name
    if search.isnumeric(): #проверяю, является ли вводимое значение числом
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.id == search).all()
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <10} | {date}')
    else:
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.name == search).all()
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <10} | {date}')



session.close()

if __name__ == '__main__':
    get_publisher()
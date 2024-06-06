import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base() #регистрирует всех своих наследников


publisher_book = sq.Table('publisher_book', Base.metadata,
                          sq.Column('id_publisher', sq.Integer, sq.ForeignKey('publisher.id')),
                          sq.Column('id_book', sq.Integer, sq.ForeignKey('book.id'))) #многие-ко-многим


class Publisher(Base):#автор
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True, nullable=False)

    # name_publisher = relationship('Book', back_populates='publisher')
    def __str__(self):
        return f'Publisher {self.id}: {self.name}'


class Book(Base):#книга
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, unique=True, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    # publisher = relationship(Publisher, back_populates='name_publisher')
    publisher = relationship('Publisher', backref='book')

    def __str__(self):
        return f'Book {self.id}: {self.title}'


class Shop(Base):#магазин
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, unique=True, nullable=False)

    def __str__(self):
        return f'Shop {self.id}: {self.name}'


class Stock(Base):#продажа
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship('Book', backref='stock')
    shop = relationship('Shop', backref='stock', primaryjoin='Stock.id_shop == Shop.id')


class Sale(Base):#скидка
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship('Stock', backref='sale')

    def __str__(self):
        return f'Sale {self.price}: {self.date_sale}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

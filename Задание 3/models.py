import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=128), nullable=False, unique=True)
    
    book = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'publisher {self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=128), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, back_populates='book')
    stock = relationship('Stock', back_populates='book')

    def __str__(self):
        return f'book {self.id}: ({self.title}, {self.id_publisher})'
    

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, sq.CheckConstraint('count >= 0'), nullable=False)

    book = relationship(Book, back_populates='stock')
    shop = relationship('Shop', back_populates='stock')
    sale = relationship('Sale', back_populates='stock')

    def __str__(self):
        return f'stock {self.id}: ({self.id_book}, {self.id_shop}, {self.count})'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, sq.CheckConstraint('price >= 0'), nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, sq.CheckConstraint('count >= 0'), nullable=False)

    stock = relationship(Stock, back_populates="sale")


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=128), nullable=False)

    stock = relationship(Stock, back_populates="shop")

    def __str__(self):
        return f'sale {self.id}: {self.name}'

def create_tables(engine):
    Base.metadata.create_all(engine)

def delete_tables(engine):
    Base.metadata.drop_all(engine)


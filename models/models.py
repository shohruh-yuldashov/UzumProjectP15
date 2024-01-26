import enum
from datetime import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    MetaData,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    DECIMAL,
    UniqueConstraint,
    Enum, Float, DateTime, Date
)
from sqlalchemy.orm import relationship

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String),
    Column('username', String),
    Column('password', String),
    Column('balance', Float),
    Column('joined_at', TIMESTAMP, default=datetime.utcnow),
)

products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('count', Integer),
    Column('price', Float),
    Column('colour', Text),
    Column('description', String),
    Column('created_at', DateTime)
)

delivery = Table(
    'delivery',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('status', Integer, ForeignKey('status.id'))
)

credit_choice = Table(
    'credit_choice',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('choice', Integer, default=12)
)

credit = Table(
    'credit',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('choice', Integer, ForeignKey('credit_choice.id')),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)


class PaymentEnum(enum.Enum):
    active = 'processing'
    payed = 'payed'


user_payment = Table(
    'user_payment',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('payment_for_month', Float),
    Column('payment_price', Float),
    Column('payed_amount', Float),
    Column('payed_month', Integer),
    Column('credit_id', Integer, ForeignKey('credit.id')),
    Column('status', Enum(PaymentEnum), default=PaymentEnum.active),
    Column('created_at', TIMESTAMP, default=datetime.utcnow)
)

shopping_cart = Table(
    'shopping_cart',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('expires_at', DateTime),
    Column('count', Integer),
)

question = Table(
    'question_and_answer',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('question', Text),
    Column('answer', Text)
)

promocodes = Table(
    'promocodes',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
    Column('date', DateTime)
)

# categories = Table(
#     'categories',

city = Table(
    'city',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
)

# subcategories = Table(
#     'subcategories',

regions = Table(
    'regions',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
)
#
# category_products = Table(
#     'category_products',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('product_id', Integer, ForeignKey('products.id')),
#     Column('category_id', Integer, ForeignKey('categories.id')),
#     Column('subcategory_id', Integer, ForeignKey('subcategories.id'))
# )

status = Table(
    'status',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Integer),
)

# like = Table(
#     'like',
order = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)

# comment = Table(
#     'comment',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('product_id', Integer, ForeignKey('products.id')),
#     Column('comment', Text),
#     Column('location_id', Integer, ForeignKey('location.id')),
#     Column('created_at', TIMESTAMP, default=datetime.utcnow),
# )

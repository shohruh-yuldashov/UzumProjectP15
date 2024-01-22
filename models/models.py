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
    Enum, Float, DateTime
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

credit = Table(
    'credit',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('name', Text),
    Column('deadline', DateTime),
)

<<<<<<< Updated upstream

shopping_cart = Table(
    'shopping_cart',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('expires_at', DateTime),
    Column('count', Integer),
=======
question = Table(
    'question_and_answer',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('question', Text),
    Column('answer', Text),
>>>>>>> Stashed changes
)


promocodes = Table(
    'promocodes',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
    Column('date', DateTime)
)

<<<<<<< Updated upstream

categories = Table(
    'categories',
=======
city = Table(
    'city',
>>>>>>> Stashed changes
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
)

<<<<<<< Updated upstream

subcategories = Table(
    'subcategories',
=======
regions = Table(
    'regions',
>>>>>>> Stashed changes
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
)

<<<<<<< Updated upstream

category_products = Table(
    'category_products',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('subcategory_id', Integer, ForeignKey('subcategories.id'))
)


status = Table(
    'status',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Integer),
)


like = Table(
    'like',
=======
order = Table(
    'order',
>>>>>>> Stashed changes
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
<<<<<<< Updated upstream
    Column('created_at', datetime.utcnow),
)

comment = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('comment', Text),
    Column('created_at', datetime.utcnow),
)
=======
    Column('location_id', Integer, ForeignKey('location.id')),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)
>>>>>>> Stashed changes

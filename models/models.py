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
    Enum, Float, DateTime, TIME
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
    Column('joined_at', TIMESTAMP, default=datetime.utcnow)
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
    Column('deadline', DateTime)
)


shopping_cart = Table(
    'shopping_cart',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('expires_at', TIMESTAMP, default=datetime.utcnow),
    Column('count', Integer)
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
    Column('price', Integer),
    Column('date', DateTime)
)

categories = Table(
    'categories',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text)
)

city = Table(
    'city',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
    Column('region_id', Integer, ForeignKey('regions.id'))
)

subcategories = Table(
    'subcategories',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
)

regions = Table(
    'regions',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text)
)

  
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
    Column('name', Integer)
)

like = Table(
    'like',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('created_at', TIMESTAMP, default=datetime.utcnow)
)

order = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('created_at',TIMESTAMP, default=datetime.utcnow),
    Column('created_at', TIMESTAMP, default=datetime)
)

locations = Table(
    'locations',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text),
    Column('longitude', Float),
    Column('latitude', Float),
    Column('city_id', Integer, ForeignKey('city.id')),
    Column('opens_at', TIME),
    Column('closes_at', TIME),
    Column('has_dressing_room', Boolean, default=False)

)

comment = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('comment', Text),
    Column('created_at', TIMESTAMP, default=datetime.utcnow)
)

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
    Column('status', Integer)
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

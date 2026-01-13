
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from sqlalchemy.types import Float



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class= Base)

service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

service_inventory = db.Table(
    'service_invertory',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('part_id', db.ForeignKey('inventory.id'))
)

class Customer(Base):
    __tablename__='customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List['Service']] = db.relationship(back_populates='customer')

class Service(Base):
    __tablename__='service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(360), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False, default=date.today)
    service_desc: Mapped[str] = mapped_column(db.String(600), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanics, back_populates='service_tickets')
    inventory: Mapped[List['Inventory']] = db.relationship(secondary=service_inventory, back_populates='service_tickets')

class Mechanic(Base):
    __tablename__='mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(Float, nullable=False)

    service_tickets: Mapped[List['Service']] = db.relationship(secondary=service_mechanics, back_populates='mechanics')

class Inventory(Base):
    __tablename__='inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    service_tickets: Mapped[List['Service']] = db.relationship(secondary=service_inventory, back_populates='inventory')
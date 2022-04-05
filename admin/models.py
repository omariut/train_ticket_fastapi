from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship

from database import Base


class Station (Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) 
    slug = Column(String, unique=True, index=True) 
    location = Column(String, index=True)


class Train (Base):
    __tablename__ = 'trains'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # sonar bangla
    slug = Column(String, unique=True, index=True) 

    carts = relationship("Cart", back_populates="train")
    coaches = relationship("Coach", back_populates="train")

class Coach (Base):
    __tablename__ = 'coaches'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) 
    slug = Column(String, unique=True, index=True)

    dep_st_id = Column(Integer, ForeignKey("stations.id"))
    dep_st = relationship("Station", foreign_keys=[dep_st_id])
    dep_time =  Column(Time)

    des_st_id = Column(Integer, ForeignKey("stations.id"))
    des_st = relationship("Station", foreign_keys=[des_st_id])
    des_time = Column(Time)
    
    train_id = Column(Integer, ForeignKey("trains.id"))
    train = relationship("Train", back_populates="coaches")
    tickets = relationship("Ticket", back_populates="coach")

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True) # ka , kha etc

    train_id = Column(Integer, ForeignKey("trains.id"))
    train = relationship("Train", back_populates="carts")

    seats = relationship("Seat", back_populates="cart")

class Seat(Base):
    __tablename__ = 'seats'
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True) # H1, H2 etc
    cart_id = Column(Integer, ForeignKey("carts.id"))
    cart = relationship("Cart", back_populates="seats")
    tickets = relationship("Ticket", back_populates="seat")
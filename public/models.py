from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Ticket (Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    
    coach_name = Column(String, ForeignKey("coaches.name"))
    coach = relationship("Coach", back_populates="tickets")

    seat_number = Column(String, ForeignKey("seats.number"))
    seat = relationship("Seat", back_populates="tickets")





from sqlalchemy.orm import Session
from . import models, schemas
from base.utils import slugify

# ***********************Tickets*****************************
#CREATE
def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(**ticket.dict() )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

#READ
def get_ticket(db: Session, ticket_id: int):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    return ticket

def get_ticket_by_seat_number_and_coach_name(db: Session, number : str, coach_name : str ):
    ticket = db.query(models.Ticket).filter(models.Ticket.seat_number == number, models.Ticket.coach_name == coach_name ).first()
    return ticket

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()

#UPDATE
def update_ticket(db: Session, ticket_id: int,  ticket_data: schemas.TicketCreate):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    ticket.name = ticket_data.name
    ticket.location = ticket_data.location
    db.commit()
    db.refresh(ticket)
    print(ticket)
    return ticket

#DELETE
def delete_ticket(db: Session, ticket_id: int):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    db.delete(db_ticket)
    db.commit()
    return get_tickets(db = db)


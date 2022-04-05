from typing import List
import time
import asyncio
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from  base.utils import slugify
from  public import crud, models, schemas
from  database import SessionLocal, engine
from fastapi import APIRouter
models.Base.metadata.create_all(bind=engine)
ticket_router = APIRouter( tags=["Ticket"], )


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ***********************Tickets*****************************

#CREATE
@ticket_router.post("/tickets/", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket_by_seat_number_and_coach_name(db, number = ticket.seat_number , coach_name = ticket.coach_name)
    if db_ticket:
        raise HTTPException(status_code=400, detail="Ticket already booked")
    return crud.create_ticket(db=db, ticket=ticket)


#READ
@ticket_router.get("/tickets/", response_model=List[schemas.TicketResponse])
async def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets


@ticket_router.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

#UPDATE
@ticket_router.put("/tickets/update/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(ticket_id:int,ticket_data: schemas.TicketCreate, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=400, detail="Ticket doesn't exist")
    db_ticket = crud.update_ticket(db, ticket_id, ticket_data=ticket_data)
    return db_ticket

#DELETE
@ticket_router.post("/tickets/delete/{ticket_id}")
def delete_ticket(ticket_id:int, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=400, detail="Ticket doesn't exist")
    crud.delete_ticket(db, ticket_id)

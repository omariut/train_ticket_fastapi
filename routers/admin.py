from typing import List
import time
import asyncio
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from  base.utils import slugify
from  admin import crud, models, schemas
from  database import SessionLocal, engine
from fastapi import APIRouter
models.Base.metadata.create_all(bind=engine)

station_router = APIRouter( tags=["Station"], )
train_router = APIRouter(tags=["Train"],)
cart_router = APIRouter(tags=["Cart"],)
coach_router = APIRouter(tags=["Couch"],)
seat_router = APIRouter(tags=["Seat"],)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ***********************Stations*****************************

#CREATE
@station_router.post("/stations/", response_model=schemas.StationResponse)
def create_station(station: schemas.StationCreate, db: Session = Depends(get_db)):
    slug = slugify(station.name)
    db_station = crud.get_station_by_slug(db, slug=slug)
    if db_station:
        raise HTTPException(status_code=400, detail="Station already registered")
    return crud.create_station(db=db, station=station)


#READ
@station_router.get("/stations/", response_model=List[schemas.StationResponse])
async def read_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stations = crud.get_stations(db, skip=skip, limit=limit)
    return stations


@station_router.get("/stations/{station_id}", response_model=schemas.StationResponse)
def read_station(station_id: int, db: Session = Depends(get_db)):
    db_station = crud.get_station(db, station_id=station_id)
    if db_station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return db_station

#UPDATE
@station_router.put("/stations/update/{station_id}", response_model=schemas.StationResponse)
def update_station(station_id:int,station_data: schemas.StationCreate, db: Session = Depends(get_db)):
    db_station = crud.get_station(db, station_id=station_id)
    if not db_station:
        raise HTTPException(status_code=400, detail="Station doesn't exist")
    db_station = crud.update_station(db, station_id, station_data=station_data)
    return db_station

#DELETE
@station_router.post("/stations/delete/{station_id}")
def delete_station(station_id:int, db: Session = Depends(get_db)):
    db_station = crud.get_station(db, station_id=station_id)
    if not db_station:
        raise HTTPException(status_code=400, detail="Station doesn't exist")
    crud.delete_station(db, station_id)


# ***********************Train*****************************

#CREATE
@train_router.post("/trains/", response_model=schemas.TrainResponse)
def create_train(train: schemas.TrainCreate, db: Session = Depends(get_db)):
    slug = slugify(train.name)
    db_train = crud.get_train_by_slug(db, slug=slug)
    if db_train:
        raise HTTPException(status_code=400, detail="Train already registered")
    return crud.create_train(db=db, train=train)

#READ
@train_router.get("/trains/", response_model=List[schemas.TrainResponse])
def read_trains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trains = crud.get_trains(db, skip=skip, limit=limit)
    return trains


@train_router.get("/trains/{train_id}", response_model=schemas.TrainResponse)
def read_train(train_id: int, db: Session = Depends(get_db)):
    db_train = crud.get_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(status_code=404, detail="Train not found")
    return db_train

#UPDATE
@train_router.put("/trains/update/{train_id}", response_model=schemas.TrainResponse)
def update_train(train_id:int,train_data: schemas.TrainCreate, db: Session = Depends(get_db)):
    db_train = crud.get_train(db, train_id=train_id)
    if not db_train:
        raise HTTPException(status_code=400, detail="Train doesn't exist")
    db_train = crud.update_train(db, train_id, train_data=train_data)
    return db_train

#DELETE
@train_router.post("/trains/delete/{train_id}")
def delete_train(train_id:int, db: Session = Depends(get_db)):
    db_train = crud.get_train(db, train_id=train_id)
    if not db_train:
        raise HTTPException(status_code=400, detail="Train doesn't exist")
    crud.delete_train(db, train_id)



# ***********************Cart*****************************

#CREATE
@cart_router.post("/carts/", response_model=schemas.CartResponse)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(get_db)):
    db_cart = crud.get_cart_by_slug(db, slug=cart.slug)
    if db_cart:
        raise HTTPException(status_code=400, detail="Cart already registered")
    db_cart = crud.create_cart(db=db, cart=cart)
    db_cart.train_name = db.query(models.Train).filter(models.Train.id == db_cart.train_id).first().name
    return db_cart

#READ
@cart_router.get("/carts/", response_model=List[schemas.CartResponse])
def read_carts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    carts = crud.get_carts(db, skip=skip, limit=limit)
    return carts


@cart_router.get("/carts/{cart_id}", response_model=schemas.CartResponse)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db, cart_id=cart_id)

    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    if db_cart.train_id:
        train_name = crud.get_train(db, train_id=db_cart.train_id)
        db_cart.train_name = train_name

    return db_cart

#UPDATE
@cart_router.put("/carts/update/{cart_id}", response_model=schemas.CartResponse)
def update_cart(cart_id:int,cart_data: schemas.CartCreate, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db, cart_id=cart_id)
    if not db_cart:
        raise HTTPException(status_code=400, detail="Cart doesn't exist")
    db_cart = crud.update_cart(db, cart_id, cart_data=cart_data)
    return db_cart

#DELETE
@cart_router.post("/carts/delete/{cart_id}")
def delete_cart(cart_id:int, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db, cart_id=cart_id)
    if not db_cart:
        raise HTTPException(status_code=400, detail="Cart doesn't exist")
    crud.delete_cart(db, cart_id)



# ***********************Couch*****************************

#CREATE
@coach_router.post("/coaches/", response_model=schemas.CoachResponse)
def create_coach(coach: schemas.CoachCreate, db: Session = Depends(get_db)):
    db_coach = crud.get_coach_by_name(db, name=coach.name)
    if db_coach:
        raise HTTPException(status_code=400, detail="Coach already registered")
    return crud.create_coach(db=db, coach=coach)

#READ
@coach_router.get("/coaches/", response_model=List[schemas.CoachResponse])
def read_coaches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coaches = crud.get_coaches(db, skip=skip, limit=limit)
    return coaches


@coach_router.get("/coaches/{coach_id}", response_model=schemas.CoachResponse)
def read_coach(coach_id: int, db: Session = Depends(get_db)):
    db_coach = crud.get_coach(db, coach_id=coach_id)

    if db_coach is None:
        raise HTTPException(status_code=404, detail="Coach not found")
    return db_coach

#DELETE
@coach_router.post("/coaches/delete/{coach_id}")
def delete_coach(coach_id:int, db: Session = Depends(get_db)):
    db_coach = crud.get_coach(db, coach_id=coach_id)
    if not db_coach:
        raise HTTPException(status_code=400, detail="Coach doesn't exist")
    crud.delete_coach(db, coach_id)





# ***********************Seat*****************************

#CREATE
@seat_router.post("/seats/", response_model=schemas.SeatResponse)
def create_seat(seat: schemas.SeatCreate, db: Session = Depends(get_db)):
    db_seat = crud.get_seat_by_number(db, number=seat.number)
    if db_seat:
        raise HTTPException(status_code=400, detail="Seat already registered")
    return crud.create_seat(db=db, seat=seat)

#READ
@seat_router.get("/seats/", response_model=List[schemas.SeatResponse])
def read_seats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    seats = crud.get_seats(db, skip=skip, limit=limit)
    return seats


@seat_router.get("/seats/{seat_id}", response_model=schemas.SeatResponse)
def read_seat(seat_id: int, db: Session = Depends(get_db)):
    db_seat = crud.get_seat(db, seat_id=seat_id)

    if db_seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return db_seat

#DELETE
@seat_router.post("/seats/delete/{seat_id}")
def delete_seat(seat_id:int, db: Session = Depends(get_db)):
    db_seat = crud.get_seat(db, seat_id=seat_id)
    if not db_seat:
        raise HTTPException(status_code=400, detail="Seat doesn't exist")
    crud.delete_seat(db, seat_id)
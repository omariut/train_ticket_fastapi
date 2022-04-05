from sqlalchemy.orm import Session
from . import models, schemas
from base.utils import slugify

# ***********************Stations*****************************
#CREATE
def create_station(db: Session, station: schemas.StationCreate):
    db_station = models.Station(**station.dict(), slug=slugify(station.name) )
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station

#READ
def get_station(db: Session, station_id: int):
    station = db.query(models.Station).filter(models.Station.id == station_id).first()
    return station

def get_station_by_slug(db: Session, slug : str):
    station = db.query(models.Station).filter(models.Station.slug == slug).first()
    return station

def get_stations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Station).offset(skip).limit(limit).all()

#UPDATE
def update_station(db: Session, station_id: int,  station_data: schemas.StationCreate):
    station = db.query(models.Station).filter(models.Station.id == station_id).first()
    station.name = station_data.name
    station.location = station_data.location
    db.commit()
    db.refresh(station)
    print(station)
    return station

#DELETE
def delete_station(db: Session, station_id: int):
    db_station = db.query(models.Station).filter(models.Station.id == station_id).first()
    db.delete(db_station)
    db.commit()
    return get_stations(db = db)



# ***********************Trains*****************************

#CREATE
def create_train(db: Session, train: schemas.TrainCreate):
    db_train = models.Train(**train.dict(), slug=slugify(train.name) )
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    return db_train

#READ
def get_train(db: Session, train_id: int):
    train = db.query(models.Train).filter(models.Train.id == train_id).first()
    return train

def get_train_by_slug(db: Session, slug : str):
    train = db.query(models.Train).filter(models.Train.slug == slug).first()
    return train

def get_trains(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Train).offset(skip).limit(limit).all()

#UPDATE
def update_train(db: Session, train_id: int,  train_data: schemas.TrainCreate):
    train = db.query(models.Train).filter(models.Train.id == train_id).first()
    train.name = train_data.name
    db.commit()
    db.refresh(train)
    print(train)
    return train

#DELETE
def delete_train(db: Session, train_id: int):
    db_train = db.query(models.Train).filter(models.Train.id == train_id).first()
    db.delete(db_train)
    db.commit()
    return get_trains(db = db)

# ***********************Carts*****************************

#CREATE
def create_cart(db: Session, cart: schemas.CartCreate):
    db_cart = models.Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

#READ
def get_cart(db: Session, cart_id: int):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    return cart

def get_cart_by_slug(db: Session, slug : str):
    cart = db.query(models.Cart).filter(models.Cart.slug == slug).first()
    return cart

def get_carts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cart).offset(skip).limit(limit).all()

#UPDATE
def update_cart(db: Session, cart_id: int,  cart_data: schemas.CartCreate):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    cart.train_id = cart_data.train_id
    db.commit()
    db.refresh(cart)
    print(cart)
    return cart

#DELETE
def delete_cart(db: Session, cart_id: int):
    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    db.delete(db_cart)
    db.commit()
    return get_carts(db = db)

# ***********************Coach*****************************

#CREATE
def create_coach(db: Session, coach: schemas.CoachCreate):
    db_coach = models.Coach(**coach.dict())
    db.add(db_coach)
    db.commit()
    db.refresh(db_coach)
    return db_coach

#READ
def get_coach(db: Session, coach_id: int):
    coach = db.query(models.Coach).filter(models.Coach.id == coach_id).first()
    return coach

def get_coach_by_name(db: Session, name : str):
    coach = db.query(models.Coach).filter(models.Coach.name == name).first()
    return coach

def get_coaches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Coach).offset(skip).limit(limit).all()

#UPDATE


#DELETE
def delete_coach(db: Session, coach_id: int):
    db_coach = db.query(models.Coach).filter(models.Coach.id == coach_id).first()
    db.delete(db_coach)
    db.commit()
    return get_coaches(db = db)


# ***********************Seat*****************************

#CREATE
def create_seat(db: Session, seat: schemas.SeatCreate):
    db_seat = models.Seat(**seat.dict())
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

#READ
def get_seat(db: Session, seat_id: int):
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    return seat

def get_seat_by_number(db: Session, number : str):
    seat = db.query(models.Seat).filter(models.Seat.number == number).first()
    return seat

def get_seats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Seat).offset(skip).limit(limit).all()

#UPDATE


#DELETE
def delete_seat(db: Session, seat_id: int):
    db_seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    db.delete(db_seat)
    db.commit()
    return get_seats(db = db)
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
#Station
class StationBase(BaseModel):
    name : str 
    location : Optional[str]  

class StationCreate(StationBase):
    pass

class StationResponse(StationBase):
    id : int
    slug : str
    
    class Config:
        orm_mode = True



#Train
class TrainBase(BaseModel):
    name : str 

class TrainCreate(TrainBase):
    pass

class TrainResponse(TrainBase):
    id : int
    slug : str
    
    class Config:
        orm_mode = True

#Carts
class CartBase(BaseModel):
    slug : str 
    

class CartCreate(CartBase):
   train_id : Optional[int]

class CartResponse(CartBase):
    id : int
    train : TrainBase
    
    
    class Config:
        orm_mode = True

#Coach
class CoachBase(BaseModel):
    name: str
    dep_st_id : int
    dep_time : time
    des_st_id : int
    des_time : time
    train_id : int

class CoachCreate(CoachBase):
    pass
class CoachResponse( CoachBase):
    id : int
    name: str
    train :  TrainResponse
    dep_st : StationResponse
    #dep_st_name : str
    des_st : StationResponse
    
    class Config:
        orm_mode = True

#Seat
class SeatBase(BaseModel):
    number : str
    cart_id : int

class SeatCreate(SeatBase):
    pass
class SeatResponse(SeatBase):
    cart : Optional[CartResponse]
        
    class Config:
        orm_mode = True
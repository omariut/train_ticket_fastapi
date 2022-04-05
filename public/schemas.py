from typing import List, Optional
from pydantic import BaseModel
from admin import schemas

class TicketBase(BaseModel):
    coach_name : str
    seat_number : str
class TicketCreate(TicketBase):
    pass

class TicketResponse(BaseModel):
    coach : schemas.CoachResponse
    class Config:
        orm_mode = True
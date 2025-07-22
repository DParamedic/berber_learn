from pydantic import BaseModel, ConfigDict

from app.auth.DTO import User

class Interval(BaseModel):
    length: int
    
    model_config = ConfigDict(from_attributes=True)
    
class Interval_List(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)
    
class Link_Interval_List(BaseModel):
    interval_list_id: int
    interval_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class User_Settings(BaseModel):
    user_id: int
    interval_list_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
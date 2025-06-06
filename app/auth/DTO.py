from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    name: str | None = None
    telegram_id: int
    
    model_config = ConfigDict(from_attributes=True)
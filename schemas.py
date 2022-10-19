from pydantic import BaseModel


class DefaultResponseSchema(BaseModel):
    detail: str

class UserSchema(BaseModel):
    user_id: str
    name: str
    age: int

class UserInputSchema(BaseModel):
    name: str = None
    age: int = None


class FavoriteSchema(BaseModel):
    user_id: str
    symbol: str

class DailySummary(BaseModel):
    highest: float
    lowest: float
    symbol: str

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserNew(BaseModel):
    """Sent by the client in requests to create a new user in the system"""
    username: str
    email: EmailStr
    name: str
    password: str

    class Config:
        schema_extra = {
            'example': {
                'username': 'cool_user',
                'email': 'user@mail.com',
                'name': 'User Userson Jr',
                'password': 'secretpassword',
            }
        }


class User(BaseModel):
    """User objects returned to the client"""
    username: str
    email: EmailStr
    name: str

    class Config:
        schema_extra = {
            'example': {
                'username': 'cool_user',
                'email': 'user@mail.com',
                'name': 'User Userson Jr',
            }
        }


class ItemNew(BaseModel):
    """Sent by the client in requests to create a new item in the system"""
    name: str
    price: float

    class Config:
        schema_extra = {
            'example': {
                'name': 'item 1',
                'price': 12.34,
            }
        }


class Item(BaseModel):
    """Item objects returned to the client"""
    id: str
    name: str
    owner: str
    price: float
    created: datetime
    updated: datetime

    class Config:
        schema_extra = {
            'example': {
                'id': 'JHJ454',
                'name': 'item 1',
                'owner': 'cool_user',
                'price': 12.34,
                'created': '2021-05-16 00:18:31.568334',
                'updated': '2021-05-16 00:20:31.568334',
            }
        }

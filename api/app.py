from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import add_user, get_user, get_items, get_item_by_id, add_item
from schemas import User, Item
from settings import Settings
from auth import set_secret_key, login_for_access_token, Token

settings = Settings()

set_secret_key(settings.secret_key)
app = FastAPI()

origins = [
    settings.app_origin,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Endpoints binding
app.post('/token', response_model=Token)(login_for_access_token)
app.post('/user', response_model=User)(add_user)
app.get('/user', response_model=User)(get_user)
app.get('/items', response_model=List[Item])(get_items)
app.get('/items/{item_id}', response_model=Item)(get_item_by_id)
app.post('/items', response_model=Item)(add_item)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host=settings.host, port=settings.port, log_level='info')

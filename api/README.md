# FastAPI server template

This folder contains a basic [FastAPI](https://fastapi.tiangolo.com/) app with JWT token authentication. It is intended
to be used as a template that implements and extends the concepts presented
[in the docs](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).

## Install dependencies

The usual deal in Python:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run server

Create a `.env` file as a copy of `.env.example` and modify the values to suit your case:

- SECRET_KEY: a random string to be used for JWT tokens encryption and decryption.
- HOST: the interface to listen.
- PORT: the port to bind to.
- APP_ORIGIN: URL from which client connections are expected. Required for CORS.

Just ensure you are using the proper venv and run the main file:

```shell
source venv/bin/activate
python app.py
```

You now should be able to visit the interactive [OpenAPI](https://www.openapis.org/) documentation of your server
at `http://HOST:PORT/docs`.

## Adjust the template to your use case

This repo works straight out of the box by mocking a persistance layer. In order to use it in your project, you need to
add your own database and plug it with the existing code.

This persistence requieres **at least** a way to store users with a **username** and a **password hash**. This is used
to validate clients and provide them with a valid signed JWT token.

### Configure JWT auth

Modify the contents of the `get_password_hash_for_username` function in `models_db.py` to properly retrieve password
hashes given a username. How to do this depends on your persistence layer, but it could look like this
with [SQLAlchemy](https://www.sqlalchemy.org/), for example:

```python
def get_password_hash_for_username(username: str) -> (bool, str):
    """Retrieves the hashed password of a user in the system given its username

    The function returns a tuple that contains:

    - bool: true is the username represents a user in the system
    - str: hashed password of the user, if it exists
    """
    user = session.query(UserInDB).filter_by(username=username).first()
    if user is not None:
        return True, user.password_hash
    else:
        return False, ''
```

**IMPORTANT:** You also need to ensure that the password hashes that you store in your persistence layer are created
using the `make_password_hash` function in `auth.py`, or configure the `pwd_context` object to match your hashing setup.

### (Optional) Implement the user endpoints

The template includes endpoints to create new users (POST /user) and to get the details of the currently 
logged user (GET /user). In order for them to work, you need to implement the functions `add_user` and
`get_user` from the file `endpoints.py`. Again, this may differ depending on your persistence layer, but 
it could look like this:

```python
def add_user(new_user: UserNew) -> User:
    """Add a user to the system for authentication"""
    password_hash: str = make_password_hash(new_user.password)

    db_user = ExampleDbUser(
        username=new_user.username,
        email=new_user.email,
        name=new_user.name,
        password_hash=password_hash,
    )

    success = add_user_to_db(db_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Could not create the user',
        )

    user = User(
        username=new_user.username,
        email=new_user.email,
        name=new_user.name,
    )

    return user


def get_user(username: str = Depends(get_current_username)) -> User:
    """Retrieve info from the currently logged user. Requires authentication."""

    found, db_user = get_user_from_db(username)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found with username "{username}"',
        )

    user = User(db_user)  # Transform from DB model to API model

    return user
```

### Add a new endpoint

First add the needed API models to `models_api.py` as [Pydantic](https://pydantic-docs.helpmanual.io/)
classes. These are not persistence models, they are just used for receiving and returning data in the HTTP calls.
However, it should be easy to connect the Pydantic classes with your persistence layer.

Example:

```python
from datetime import datetime
from pydantic import BaseModel


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
```

Then add a function to process a request in `endpoints.py`. If the request doesn't need authentication, just do
something like this:

```python
from typing import List
from models_api import Item


def get_items() -> List[Item]:
    """Retrieve a list of all the items in the system"""
    items = []  # Retrieve from your persistence layer
    return items
```

Or if you need to ensure that the client is authenticated, or you need to know who they are, add a FastAPI dependency to
the `get_current_username` function defined in `auth.py`. This way, your function will receive the username as a
parameter, if the authentication succeeded, or the client will receive a 402 UNAUTHORIZED error:

```python
from fastapi import Depends
from models_api import ItemNew, Item
from auth import get_current_username


def add_item(new_item: ItemNew, username: str = Depends(get_current_username)) -> Item:
    """Add a new item to the system and marks it as owned by the current user. Requires authentication"""
    now = datetime.now()
    item = Item(
        id='new id',
        name=new_item.name,
        owner=username,
        price=new_item.price,
        created=now,
        updated=now,
    )

    # Persist this new info into your persistence layer

    return item
```

Finally, bind the functions to the proper endpoints in the `app.py` file:

```python
...

app.get('/items', response_model=List[Item])(get_items)
app.post('/items', response_model=Item)(add_item)

...
```

This example is represented and extended in the repo files.

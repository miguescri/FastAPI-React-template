from datetime import datetime, timedelta
from typing import List
from fastapi import Depends, HTTPException, status

from auth import get_current_username, make_password_hash
from models_api import UserNew, User, ItemNew, Item


def add_user(new_user: UserNew) -> User:
    """Add a user to the system for authentication"""
    password_hash: str = make_password_hash(new_user.password)
    # TODO: persist user with hashed_password in your database

    user = User(
        username=new_user.username,
        email=new_user.email,
        name=new_user.name,
    )

    return user


def get_user(username: str = Depends(get_current_username)) -> User:
    """Retrieve info from the currently logged user. Requires authentication."""
    # TODO: retrieve user with username from database

    user = User(
        username=username,
        email='user@mail.com',
        name='User Userson Jr',
    )
    return user


# TODO: implement database logic to substitute this mockup list
now = datetime.now()
items = [
    Item(
        id='00001',
        name='Item 1',
        owner='a_user',
        price=10.5,
        created=(now - timedelta(days=3)),
        updated=(now - timedelta(days=1)),
    ),
    Item(
        id='00002',
        name='Item 2',
        owner='another_user',
        price=0.5,
        created=(now - timedelta(days=10)),
        updated=(now - timedelta(days=5)),
    ),
    Item(
        id='00003',
        name='Item 3',
        owner='third_user',
        price=5,
        created=(now - timedelta(days=1)),
        updated=(now - timedelta(hours=3)),
    ),
]


def get_items() -> List[Item]:
    """Retrieve a list of all the items in the system"""
    return items


def get_item_by_id(item_id: str) -> Item:
    """Retrieve an item given its ID"""
    for item in items:
        if item.id == item_id:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item not found with id "{item_id}"',
        )


def add_item(new_item: ItemNew, username: str = Depends(get_current_username)) -> Item:
    """Add a new item to the system and marks it as owned by the current user. Requires authentication"""
    now = datetime.now()
    item = Item(
        id=str(len(items) + 1).zfill(5),
        name=new_item.name,
        owner=username,
        price=new_item.price,
        created=now,
        updated=now,
    )
    items.append(item)

    return item

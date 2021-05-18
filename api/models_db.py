from typing import List

from pydantic import BaseModel, EmailStr


# THIS IS AN IMPORTANT FUNCTION. DO NOT DELETE. IMPLEMENT IT PROPERLY
def get_password_hash_for_username(username: str) -> (bool, str):
    """Retrieve the hashed password of a user in the system given its username

    The function returns a tuple that contains:

    - bool: true is the username represents a user in the system
    - str: hashed password of the user, if it exists
    """
    # TODO: implement here your database logic to retrieve the hash
    found, user = get_user_from_db(username)
    if found:
        return True, user.password_hash
    else:
        return False, ''


# ALL THE FOLLOWING IS MOCKUP CODE

# TODO: define a proper persistence layer for your users
class ExampleDbUser(BaseModel):
    username: str
    email: EmailStr
    name: str
    password_hash: str


example_user_list: List[ExampleDbUser] = []


def add_user_to_db(new_user: ExampleDbUser) -> bool:
    """Add a user to the databse. username must me unique

    If the user is properly added, returns True. Otherwise, returns False
    """
    for user in example_user_list:
        if user.username == new_user.username:
            return False
    else:
        example_user_list.append(new_user)
        return True


def get_user_from_db(username: str) -> (bool, ExampleDbUser):
    """Retrieve a user from the database given its username

    Returns a tuple:

    - bool: true is user was found
    - ExampleDbUser: contains the user, if found
    """
    for user in example_user_list:
        if user.username == username:
            return True, user
    else:
        return False, ExampleDbUser()

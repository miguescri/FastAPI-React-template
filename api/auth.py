from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from models_db import get_password_hash_for_username

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    """Object returned when authentication succeeds.

    - access_token: contains a JWT token for HTTP header authentication
    - token_type: usually "bearer"
    """
    access_token: str
    token_type: str


secret_key: str = 'secret'
pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='token')


def set_secret_key(key: str) -> None:
    """Configure the secret key used for token encryption and decryption"""
    global secret_key
    secret_key = key


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that the plain password results in the provided hash"""
    return pwd_context.verify(plain_password, hashed_password)


def make_password_hash(password: str) -> str:
    """Generate a salted hash for the password"""
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> bool:
    """Verify if there is a user in the system  with the given username:password combination"""
    user_exists: bool
    password_hash: str
    user_exists, password_hash = get_password_hash_for_username(username)
    return user_exists and verify_password(password, password_hash)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Generate a JWT token with the given data that expires after the given timedelta"""
    global secret_key

    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt: str = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Process a OAuth2 request for authentication and returns a JWT token if it is successful.
    The request must contain at least the fields username and password.

    If the provided information isn't valid, returns a 401 UNAUTHORIZED error.
    """
    username: str = form_data.username
    password: str = form_data.password
    valid: bool = authenticate_user(username, password)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = create_access_token(
        data={'sub': username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer')


def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    """Retrieve the username of the currently logged user.

    The request must contain a valid JWT token in the header. Otherwise, it will return a 401 UNAUTHORIZED error.
    """
    global secret_key

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload: dict = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return username

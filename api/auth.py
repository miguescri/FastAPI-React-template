from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


secret_key: str = 'secret'
pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='token')


def set_secret_key(key: str) -> None:
    global secret_key
    secret_key = key


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def make_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_password_hash_for_username(username: str) -> (bool, str):  # (user_exists, pwd_hash)
    # TODO: implement here your database logic to retrieve the hash
    if username == 'user':
        return True, make_password_hash('password')
    return False, None


def authenticate_user(username: str, password: str) -> bool:
    user_exists: bool
    password_hash: str
    user_exists, password_hash = get_password_hash_for_username(username)
    return user_exists and verify_password(password, password_hash)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    global secret_key

    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt: str = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
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

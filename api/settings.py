from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    host: str
    port: int
    app_origin: str

    class Config:
        env_file = '.env'

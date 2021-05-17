from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host=settings.host, port=settings.port, log_level='info')

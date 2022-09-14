from fastapi import FastAPI
from app import api

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация',
    },
{
        'name': 'user',
        'description': 'Возможности пользователей',
    },
{
        'name': 'admin',
        'description': 'Возможности админа',
    },
]

app = FastAPI(
    title='TestApp',
    version= '1.0',
    description='Реализация REST API тестового задания',
    openapi_tags=tags_metadata,
    )

app.include_router(api.router)
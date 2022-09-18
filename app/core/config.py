from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Union
from fastapi_mail import ConnectionConfig
import os
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    database_url: str = f"postgresql://{os.getenv('USER_NAME')}" \
                        f":{os.getenv('DATABASE_PASSWORD')}" \
                        f"@{os.getenv('DATABASE_HOST')}" \
                        f":{os.getenv('DATABASE_PORT')}" \
                        f"/{os.getenv('DATABASE_NAME')}" #postgresql://postgres:1007@localhost:5432/postgres

    jwt_secret: str = os.getenv('JWT_SECRET')
    jwt_algorithm: str = os.getenv('JWT_ALGORITHM')
    jwt_expires_s: int = os.getenv('JWT_EXPIRES_S')

    FIRST_SUPERUSER: EmailStr = os.getenv('FIRST_SUPERUSER')
    HOST: str = os.getenv('HOST')
    PORT: int = os.getenv('PORT')
    DEBUG: bool = True

    conf = ConnectionConfig(
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_FROM=os.getenv('MAIL_FROM'),
        MAIL_PORT=os.getenv('MAIL_PORT'),
        MAIL_SERVER=os.getenv('MAIL_SERVER'),
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        TEMPLATE_FOLDER=os.getenv('TEMPLATE_FOLDER'),
    )


    class Config:
        case_sensitive = True


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)


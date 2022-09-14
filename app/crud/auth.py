from datetime import (
    datetime,
    timedelta,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
    Request,
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
from typing import Optional, List
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.models import model_db
from app.db.database import get_session
from app.core.config import settings
from app.schemas import (users)
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema
import asyncio


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


def get_current_user(token: str = Depends(oauth2_scheme)) -> users.User:
    return AuthService.verify_token(token)


class AuthService: #класс реализующий все методы по авторизации и аутентификации
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> users.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
             payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')
        try:
            user = users.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: model_db.User) -> users.Token:
        user_data = users.User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': str(user_data.user_id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return users.Token(access_token=token)

    @staticmethod
    async def send_email(user, token):
        message = MessageSchema(
            subject='Account Verification Email',
            recipients=[user.email],
            template_body={"token": token.access_token},
            subtype='html'
        )
        fm = FastMail(settings.conf)
        await fm.send_message(message, template_name='email.html')

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(
        self,
        user_data: users.UserCreate,
        request: Request,
    ) -> users.Token:
        self.checking_for_unique(user_data.username, user_data.email)
        user = model_db.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
            )
        self.session.add(user)
        self.session.commit()
        new_token = self.create_token(user)
        asyncio.run(self.send_email(user, new_token))
        return new_token

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> users.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        exception_active = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Your email has not been verified. Check email',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = (
            self.session
            .query(model_db.User)
            .filter(model_db.User.username == username)
            .first()
        )
        if not user:
            raise exception
        if not self.verify_password(password, user.password_hash):
            raise exception
        if not user.is_active:
            raise exception_active
        return self.create_token(user)

    def checking_for_unique(self,
                            username: str,
                            email: str,
    ) -> Optional[model_db.User]:
        checking_username = (
            self.session
            .query(model_db.User)
            .filter(
                model_db.User.username == username,
             )
            .first()
        )
        checking_email = (
            self.session
            .query(model_db.User)
            .filter(
                model_db.User.email == email,
            )
            .first()
        )
        if checking_username or checking_email:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = 'Имя пользователя или e-mail уже используются, выберите другие',
            headers = {'WWW-Authenticate': 'Bearer'},
            )
        return checking_username, checking_email

    def email_verification(self, request, token):
        templates = Jinja2Templates(directory="templates")
        user = AuthService.verify_token(token)
        if user and not user.is_active:
            self.session.query(model_db.User)\
                .filter(model_db.User.email == user.email) \
                .update({'is_active': True})
            self.session.commit()
            return templates.TemplateResponse("verification.html",
                                              {"request": request, "username": user.username})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token or expired token',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class RoleChecker:  #класс реализующий управление доступом
    def __init__(self, is_superuser: List):
        self.is_superuser = is_superuser

    def __call__(self, user: users.User = Depends(get_current_user)):
        if user.is_superuser not in self.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
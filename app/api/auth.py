from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
)

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from app.schemas import users
from app.crud.auth import (AuthService,
                           get_current_user,
)

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post(
    '/sign-up/',
    response_model=users.Token,
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
    request: Request,
    user_data: users.UserCreate,
    auth_service: AuthService = Depends(),
):
    return auth_service.register_new_user(user_data, request)


@router.post(
    '/sign-in/',
    response_model=users.Token,
)
def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(
        auth_data.username,
        auth_data.password,
    )


@router.get(
    '/user/',
    response_model=users.User,
)
def get_user(user: users.User = Depends(get_current_user)):
    return user

@router.get(
    '/verification/',
    response_class=HTMLResponse,
)
async def verification(
    request: Request,
    token: str,
    auth_service: AuthService = Depends()
):
    return auth_service.email_verification(request, token)

from fastapi import APIRouter, Depends, HTTPException

# from .dependencies import user_authenticate, user_active
from .. import crud
from ..dependencies.db import get_session
from ..schemas import UserCreate, User, TokenOut


router = APIRouter(prefix='/user')


@router.post('/register', response_model=User)
def register(
        user: UserCreate,
        session=Depends(get_session),
):
    user_db = crud.user.get_by_email(session, user.email)

    if user_db:
        raise HTTPException(
            status_code=401,
            detail='Email already registered',
        )

    return crud.user.create(session, user)


# @router.post('/login', response_model=TokenOut)
# def login():
#     pass
#
#
# @router.post('/test')
# def test():
#     pass

from sqlalchemy.orm import Session

from .. import schemas
from ..database import models


def get(
        db: Session,
        user_id: int,
):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_by_email(
        db: Session,
        email: str,
):
    return db.query(models.User).filter(models.User.email == email).first()


def get_multi(
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    return db.query(models.User).offset(skip).limit(limit).all()


def create(
        db: Session,
        user: schemas.UserCreate,
):
    fake_hashed_password = user.password + "notreallyhashed"  # TODO
    db_user = models.User(email=user.email, password_hash=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

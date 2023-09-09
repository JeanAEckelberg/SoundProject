import hashlib

from sqlalchemy import and_
from sqlalchemy.orm import Session

import models
import schemas


def read_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def read_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def authenticate_user(db: Session, user: schemas.UserCreate):
    return db.query(models.User).filter(
        and_(models.User.username == user.username,
             models.User.password == hashlib.md5(user.password.encode()).hexdigest())).one_or_none()


def read_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user: models.User = models.User(**user.model_dump(exclude={'id'}))
    db_user.password = hashlib.md5(user.password.encode()).hexdigest()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, id: int, user: schemas.UserCreate):
    db_user: models.User | None = db.query(models.User).filter(models.User.id == id).one_or_none()
    if db_user is None:
        return

    for key, value in user.model_dump().items():
        setattr(db_user, key, value) if value is not None else None

    db_user.password = hashlib.md5(user.password.encode()).hexdigest()

    db.commit()
    db.refresh(db_user)
    return db_user


# Sound


def read_sound(db: Session, sound_id: int):
    return db.query(models.Sound).filter(models.Sound.id == sound_id).first()


def read_sounds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sound).offset(skip).limit(limit).all()


def create_sound(db: Session, sound: schemas.SoundBase):
    db_sound: models.Sound = models.Sound(**sound.model_dump(exclude={'id'}))
    db.add(db_sound)
    db.commit()
    db.refresh(db_sound)
    return db_sound


def update_sound(db: Session, id: int, sound: schemas.SoundBase):
    db_sound: models.Sound | None = db.query(models.Sound).filter(models.Sound.id == id).one_or_none()
    if db_sound is None:
        return

    for key, value in sound.model_dump().items():
        setattr(db_sound, key, value) if value is not None else None

    db.commit()
    db.refresh(db_sound)
    return db_sound


# user_to_sound


def read_user_to_sound(db: Session, user_to_sound_id: int):
    return db.query(models.UserToSound).filter(models.UserToSound.id == user_to_sound_id).first()


def read_users_to_sounds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserToSound).offset(skip).limit(limit).all()


def create_user_to_sound(db: Session, user_to_sound: schemas.UserToSound):
    db_user_to_sound: models.UserToSound = models.UserToSound(**user_to_sound.model_dump())
    db.add(db_user_to_sound)
    db.commit()
    db.refresh(db_user_to_sound)
    return db_user_to_sound


def update_user_to_sound(db: Session, user_id: int, sound_id, user_to_sound: schemas.UserToSound):
    db_user_to_sound: models.UserToSound | None = db.query(models.UserToSound).filter(
        and_(models.UserToSound.user_id == user_id, models.UserToSound.sound_id == sound_id)).one_or_none()

    if db_user_to_sound is None:
        return

    for key, value in user_to_sound.model_dump().items():
        setattr(db_user_to_sound, key, value) if value is not None else None

    db.commit()
    db.refresh(db_user_to_sound)
    return db_user_to_sound

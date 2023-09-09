from __future__ import annotations
from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    is_active: bool = True

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class SoundBase(BaseModel):
    id: int
    name: str
    song_data: bytes
    is_public: bool
    is_active: bool

    class Config:
        from_attributes = True


class UserSchema(UserBase):
    sounds: list[SoundBase] = []


class SoundSchema(SoundBase):
    sounds: list[UserBase] = []


class UserToSound(BaseModel):
    user_id: int
    sound_id: int
    author: bool
    listener: bool

    class Config:
        from_attributes = True

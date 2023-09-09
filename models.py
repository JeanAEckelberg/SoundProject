from __future__ import annotations
from sqlalchemy import LargeBinary, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


class UserToSound(Base):
    __tablename__ = 'user_to_sound'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    sound_id: Mapped[int] = mapped_column(ForeignKey('sounds.id'), primary_key=True)
    author = Column(Boolean)
    listener = Column(Boolean, default=True)
    users: Mapped[User] = relationship(back_populates='sound_links')
    sounds: Mapped[Sound] = relationship(back_populates='user_links')


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    sounds: Mapped[list[Sound]] = relationship(
        secondary="user_to_sound", back_populates="users", viewonly=True
    )
    sound_links: Mapped[list[UserToSound]] = relationship(back_populates='users')


class Sound(Base):
    __tablename__ = 'sounds'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    song_data = Column(LargeBinary, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    users: Mapped[list[User]] = relationship(
        secondary="user_to_sound", back_populates="sounds", viewonly=True
    )
    user_links: Mapped[list[UserToSound]] = relationship(back_populates='sounds')

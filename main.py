from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/users/", response_model=list[schemas.UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_users(db, skip, limit)


@app.post("/authenticate_user", response_model=schemas.UserSchema)
def read_user_by_auth(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return db_user


@app.post("/users/", response_model=schemas.UserSchema)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='Username already exists!')
    return crud.create_user(db, user)


@app.put("/users/{id}", response_model=schemas.UserSchema)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db, id, user)


# Sound

@app.get("/sounds/", response_model=list[schemas.SoundSchema])
def read_sounds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_sounds(db, skip, limit)


@app.post("/sounds/", response_model=schemas.SoundSchema)
def create_sound(sound: schemas.SoundBase, db: Session = Depends(get_db)):
    return crud.create_sound(db, sound)


@app.put("/sounds/{id}", response_model=schemas.SoundSchema)
def update_sound(id: int, sound: schemas.SoundBase, db: Session = Depends(get_db)):
    return crud.update_sound(db, id, sound)


# user_to_sound


@app.get("/users_to_sounds/", response_model=list[schemas.UserToSound])
def read_users_to_sounds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_users_to_sounds(db, skip, limit)


@app.post("/users_to_sounds/", response_model=schemas.UserToSound)
def create_user_to_sound(user_to_sound: schemas.UserToSound, db: Session = Depends(get_db)):
    return crud.create_user_to_sound(db, user_to_sound)


@app.put("/users_to_sounds/{user_id}/{sound_id}", response_model=schemas.UserToSound)
def update_user_to_sound(user_id: int, sound_id, user_to_sound: schemas.UserToSound, db: Session = Depends(get_db)):
    return crud.update_user_to_sound(db, user_id, sound_id, user_to_sound)

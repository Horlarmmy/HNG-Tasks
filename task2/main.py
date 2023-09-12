from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db import Base, engine, SessionLocal
from pydantic import BaseModel
import models


# Instantiate the class
app = FastAPI(
    title="HNGX",
    description="Backend Task 2",
)


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Person(BaseModel):
    name: str

@app.get("/")
def hello():
    return {"message":"Welcome!!!"}


@app.post("/api")
def details(person: Person, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.name == person.name).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    # create the user
    user = models.User(name=person.name)
    print(user.name)

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name}

@app.get("/api/{id}")
def getUser(db: Session = Depends(get_db)):
    return {"id": 1, "name": "Alade Toheeb"}

@app.delete("/api/{id}")
def delUser():
    pass

@app.put("/api/{id}")
def updateUser():
    return {"id": 1, "name": "Alade Toheeb"}
#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

#uvn helloWorld:app --reload
app = FastAPI()
#OpenAPI: conjunto de reglas para definir que una api esta bien construida
#Path parameter: este va entre llaves {xxxx}
#Query parameters: se usa para enviar informacion que no es obligatoria
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red ="red"

class Location(BaseModel):
    city: str
    state: str
    country: str


#Models

class Person(BaseModel):
    first_name: str = Field(
    ...,
    min_length = 1,
    max_length = 50,
    )
    last_name: str = Field(
    ...,
    min_length = 1,
    max_length = 50
    )
    age: int = Field(
    gt = 0,
    le = 115
    )
    hair_color: Optional[HairColor] = Field(default = None)
    is_married: Optional[bool] = Field(default = None)

    class Config:
        schema_extra = {
        "example":{
        "first_name": "zack",
        "last_name": "seneger",
        "age": 24,
        "hair_color": "black",
        "is_married": False
        }
        }


#Path operator decorator
@app.get("/")
#Path operation function
def home():
    return{"hello": "world"}

#Request and Response body

@app.post("/persona/new")
def create_preson(person: Person = Body(...)):
    return person

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
    None,
    min_length = 1,
    max_length = 50,
    title = "Person Name",
    description = "This is the person name. It's between 1 and 50 characters."
    ),
    age: str = Query(
    ...,
    title = "Person Age.",
    description = "This is the person age. It's required."
    )

    ):
    return {name : age}

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
    ...,
    gt = 0
        )
    ):
    return {person_id: "It exists!"}

@app.put("/person/{person_id}")
def update_person(
person_id: int = Path(
    ...,
    title = "Person ID",
    description = "This is the person ID",
    gt = 0
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #result = person.dict()
    #result.update(location.dict())
    #return result
    return person

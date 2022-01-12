#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import status
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form

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
class PersonBase(BaseModel):
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

class PersonOut(BaseModel):
    pass

class Person(PersonBase):
    password: str = Field(...,min_length = 8)

class LogInOut(BaseModel):
    username: str = Field(..., max_length = 20)
    message: str = Field(default = "Login succesfully!")

#Path operator decorator
@app.get(path = "/",
    status_code=status.HTTP_200_OK)
#Path operation function
def home():
    return{"hello": "world"}

#Request and Response body

@app.post(
    path = "/persona/new",
    response_model = Person,
    response_model_exclude={'password'},
    status_code = status.HTTP_201_CREATED)
def create_preson(person: Person = Body(...)):
    return person

@app.get(path = "/person/detail", 
    status_code = status.HTTP_202_ACCEPTED)
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

@app.get(
    path = "/person/detail/{person_id}",
    status_code = status.HTTP_202_ACCEPTED)
def show_person(
    person_id: int = Path(
    ...,
    gt = 0
        )
    ):
    return {person_id: "It exists!"}

@app.put(
        path = "/person/{person_id}",
        status_code = status.HTTP_202_ACCEPTED)
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

@app.post(
    path = "/login",
    response_model = LogInOut,
    status_code = status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form (...)):
    return LogInOut(username = username)
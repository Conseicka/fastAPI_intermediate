#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import status
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

#uvn helloWorld:app --reload
app = FastAPI()
#OpenAPI: conjunto de reglas para definir que una api esta bien construida
#Path parameter: este va entre llaves {xxxx}
#Query parameters: se usa para enviar informacion que no es obligatoria

#~~~~~~~~~~Models~~~~~~~~~~
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

#~~~~~~~~~~Path Operations~~~~~~~~~~

#Path operator decorator
@app.get(
    path = "/",
    status_code=status.HTTP_200_OK,
    tags = ["Home"],
    )
#Path operation function
def home():
    return{"hello": "world"}

#------------------------------------------------
#Request and Response body
#Titulo, Descripcion, Parametros, Resultado
@app.post(
    path = "/persona/new",
    response_model = Person,
    response_model_exclude={'password'},
    status_code = status.HTTP_201_CREATED,
    tags = ["Persons"],
    summary = "Create a Person in the app.",
    )
def create_preson(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the informatin in the database.

    Parameters:

    -Request Body parameter:
        -**person: Person** -> A person model with first name, last name, age, hair color and marital status.

    Retunrs a person moel with first name, last name, age, hair color and marital status.
    """
    return person

#------------------------------------------------

@app.get(
    path = "/person/detail", 
    status_code = status.HTTP_202_ACCEPTED,
    tags = ["Persons"],
    summary = "Show person details.",
    )
def show_person(
    name: Optional[str] = Query(
        default = None,
        min_length = 1,
        max_length = 50,
        title = "Person Name",
        description = "This is the person name. It's between 1 and 50 characters.",
     ),
    age: str = Query(
        ...,
        title = "Person Age.",
        description = "This is the person age. It's required."
    ),
):
    """
    Show person details
    
    This Operation shows a person details.

    Parameters:    
        -Query parameter: Person name.

    Returns a Person details.
    """
    return {name : age}

#------------------------------------------------

persons = [1, 2, 3, 4, 5]

@app.get(
    path = "/person/detail/{person_id}",
    status_code = status.HTTP_202_ACCEPTED,
    tags = ["Persons"],)
def show_person(
    person_id: int = Path(
        ...,
        gt = 0,
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "This person doesn't exist!"
        )
    return {person_id: "It exists!"}

#------------------------------------------------

@app.put(
        path = "/person/{person_id}",
        status_code = status.HTTP_202_ACCEPTED,
        tags = ["Persons"],)
def update_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        description = "This is the person ID",
        gt = 0
    ),
    person: Person = Body(...),
    #location: Location = Body(...),
):
    #result = person.dict()
    #result.update(location.dict())
    #return result
    return person

#------------------------------------------------

#Forms
@app.post(
    path = "/login",
    response_model = LogInOut,
    status_code = status.HTTP_200_OK
)
def login(
    username: str = Form(...), 
    password: str = Form (...),
):
    return LogInOut(username = username)

#cookies y header

@app.post(
    path = "/contact",
    status_code = status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        min_lenght = 1,
        max_lenght = 20
    ),
    last_name: str = Form(
        ...,
        min_lenght = 1,
        max_lenght = 20
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_lenght = 20
        ),
    user_agent: Optional [str] = Header(default = None),
    ads: Optional [str] = Cookie(default = None),
):
    return user_agent

#------------------------------------------------


@app.post(
    path = "/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename":image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1027, ndigits = 2)
    }

#------------------------------------------------
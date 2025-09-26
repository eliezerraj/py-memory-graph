from pydantic import BaseModel
from typing import List, Optional

class Person(BaseModel):
    person_id: str 

class Account(BaseModel):
    account_id: str

class Relations(BaseModel):
    description: str
    properties: dict = {}

class DataGraph(BaseModel):
    person: Optional[Person] = None
    account: Optional[Account] = None
    relations: Optional[Relations] = None

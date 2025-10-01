from pydantic import BaseModel
from typing import Optional, Any, Dict

class Person(BaseModel):
    person_id: str 

class Account(BaseModel):
    account_id: str

class Card(BaseModel):
    card_id: str

class Relations(BaseModel):
    description: str
    properties: Dict[str, Any] = {}

class DataGraph(BaseModel):
    person: Optional[Person] = None
    account: Optional[Account] = None
    relations: Optional[Relations] = None

class CardDataGraph(BaseModel):
    card: Optional[Card] = None
    account: Optional[Account] = None
    relations: Optional[Relations] = None

##----

class DataModelGraph(BaseModel):
    nodes: Dict[str, Any] = {}
    relations: Optional[Relations] = None

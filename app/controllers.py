import logging

from app.config import settings
from fastapi import FastAPI, HTTPException, Depends

from app.entities import DataGraph
from app.entities import DataModelGraph
from app.entities import Account
from app.entities import Person

from app.use_cases import GraphService
from app.adapters.neo4j_repo import Neo4jGraphRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ---------------------------------------------------------------
# methods memory
# ---------------------------------------------------------------
def get_graph_repository() -> Neo4jGraphRepository:
    """Dependency injection to get the memory repository."""

    connection_string = f"{settings.DB_HOST}:{settings.DB_PORT}"
    return Neo4jGraphRepository(connection_string, settings.DB_USER, settings.DB_PASS)

@app.get("/info")
def get_info():
    return settings

@app.get("/account/person/{person_id}", response_model=list[Account])
def get_account_from_person(person_id: str, repository: Neo4jGraphRepository = Depends(get_graph_repository)):
    """Get all accounts from given a person."""

    return GraphService(repository).get_account_from_person(person_id)

@app.get("/person/account/{account_id}", response_model=list[Person])
def get_person_from_account(account_id: str, repository: Neo4jGraphRepository = Depends(get_graph_repository)):
    """Get the persom from given an account."""

    return GraphService(repository).get_person_from_account(account_id)

#------------------------------
@app.post("/graph", response_model=DataModelGraph)
def create_graph(data_graph: DataModelGraph, repository: Neo4jGraphRepository = Depends(get_graph_repository)):
    """Create a new card graph."""

    return GraphService(repository).add_graph(data_graph)

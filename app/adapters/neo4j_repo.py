import logging

from app.entities import DataGraph
from app.entities import DataModelGraph

from typing import List, Optional
from neo4j import GraphDatabase

from app.adapters.repositories import GraphRepository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##       
class Neo4jGraphRepository(GraphRepository):
    def __init__(self, connection_string: str, username: str, password: str):
        self.connection_string = connection_string
        self.username = username
        self.password = password

    def _connect(self):
        """Create a database connection to Neo4j."""
        try:
            logger.info("Database connection Successful !!!")
            driver = GraphDatabase.driver(self.connection_string, auth=(self.username, self.password))
            return driver
        except Exception as e:
            logger.error("Database connection failed: %s", e)
            raise RuntimeError("Database connection failed") from e
          
    def get(self, cypher: str, params: dict = None) -> DataGraph:
        """Get a new graph to the database."""
        try:
            with self._connect().session() as conn:
                result = conn.run(cypher, params)
                return result.data()
        except Exception as e:
            logger.error("Error adding memory: %s", e)
            raise RuntimeError("Error get graph to the database") from e        
        
    def add_model_graph(self, cypher: str, params: dict = None) -> DataModelGraph:
        """Add a new model graph to the database."""
        try:
            with self._connect().session() as conn:
                result = conn.run(cypher, params)
                return result.data()[0]
        except Exception as e:
            logger.error("Error adding memory: %s", e)
            raise RuntimeError("Error adding model graph to the database") from e
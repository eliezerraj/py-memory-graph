import logging

from typing import List

from app.entities import DataGraph
from app.entities import Account
from app.entities import Person

from app.adapters.repositories import GraphRepository

from app.utils.converters import to_datagraph
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphService:
    def __init__(self, repository: GraphRepository):
        self.repository = repository
    
    def add_graph(self, data_graph: DataGraph) -> DataGraph:
        """Add a new graph to the repository."""
        
        formatted_time = datetime.now().strftime("%d-%m-%Y")

        data_graph.relations.properties = {"since" : formatted_time}

        params = {
            "person_id": data_graph.person.person_id,
            "account_id": data_graph.account.account_id,
            "properties": data_graph.relations.properties
        }
        
        cypher_person = f"""
                            MERGE (n:Person {{ person_id: $person_id }}) 
                            ON CREATE SET n.person_id = $person_id
                            RETURN n
        """
        response_person = self.repository.add(cypher_person, params)

        cypher_account = f"""
                            MERGE (n:Account {{ account_id: $account_id }}) 
                            ON CREATE SET n.account_id = $account_id
                            RETURN n
        """
        response_account = self.repository.add(cypher_account, params)

        cypher_relations = f"""
                            MATCH (source:Person {{person_id: $person_id}})
                            MATCH (target:Account {{account_id: $account_id}})
                            MERGE (source)-[r:{data_graph.relations.description}]->(target)
                            SET r += $properties
                            RETURN r
        """
        response_relations = self.repository.add(cypher_relations, params)

        response = to_datagraph(response_person, response_account, response_relations)
        return response

    def get_account_from_person(self, person_id: str) -> List[Account]:
        """Get all accounts from a given person."""

        params = {
            "person_id": person_id,
        }
        
        cypher_person = """
            MATCH (p:Person {person_id: $person_id})-[:HAS]->(a:Account) RETURN a
        """

        response_list = self.repository.get(cypher_person, params)
        account_list = []

        for record in response_list:
            account_data = record.get("a") 
            if account_data:
                account_list.append(Account(**account_data))

        return account_list
    
    def get_person_from_account(self, account_id: str) -> List[Person]:
        """Get the person from a given account."""

        params = {
            "account_id": account_id,
        }
        
        cypher_account = """
            MATCH (p:Person)-[:HAS]->(a:Account) 
            WHERE a.account_id = $account_id
            RETURN p
        """

        response_list = self.repository.get(cypher_account, params)
        person_list = []

        print(response_list)

        for record in response_list:
            person_data = record.get("p") 
            if person_data:
                person_list.append(Person(**person_data))

        return person_list
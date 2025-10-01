import logging

from typing import List

from app.entities import DataGraph
from app.entities import DataModelGraph
from app.entities import Account
from app.entities import Person

from app.adapters.repositories import GraphRepository

from app.utils.converters import to_datagraph, to_model_datagraph
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphService:

    def __init__(self, repository: GraphRepository):
        self.repository = repository
    
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
    
    ## --------------------------------
    def add_graph(self, data_graph: DataModelGraph) -> DataModelGraph:
        """Add nodes and their relationship to the repository (generic)."""
        
        logger.info("function => add_graph()")
        logger.info(f"data_graph: {data_graph}")

        nodes = data_graph.nodes or {}
        if len(nodes) < 2:
            logger.error(f"At least two nodes must be provided in DataGraph nodes: {nodes}")
            raise ValueError("At least two nodes must be provided in DataGraph")

        # Pick source and target (first two entries in nodes dict)
        (source_label, source_props), (target_label, target_props) = list(nodes.items())[:2]

        # Extract IDs
        source_key, source_value = next(iter(source_props.items()))
        target_key, target_value = next(iter(target_props.items()))

        params = {
            "source_props": source_props,
            "target_props": target_props,
            "properties": data_graph.relations.properties if data_graph.relations else {}
        }

        # MERGE source node
        cypher_source = f"""
            MERGE (n:{source_label.capitalize()} {{ {source_key}: $source_props.{source_key} }})
            SET n += $source_props
            RETURN properties(n) AS props, labels(n) AS labels
        """
        response_source = self.repository.add_model_graph(cypher_source, params)

        # MERGE target node
        cypher_target = f"""
            MERGE (n:{target_label.capitalize()} {{ {target_key}: $target_props.{target_key} }})
            SET n += $target_props
            RETURN properties(n) AS props, labels(n) AS labels
        """
        response_target = self.repository.add_model_graph(cypher_target, params)

        # MERGE relationship
        relation_type = data_graph.relations.description if data_graph.relations else "RELATED"
        cypher_relations = f"""
            MATCH (source:{source_label.capitalize()} {{{source_key}: $source_props.{source_key}}})
            MATCH (target:{target_label.capitalize()} {{{target_key}: $target_props.{target_key}}})
            MERGE (source)-[r:{relation_type}]->(target)
            SET r += $properties
            RETURN properties(r) AS props, type(r) AS rel_type
        """
        
        response_relations = self.repository.add_model_graph(cypher_relations, params)

        return to_model_datagraph(response_source, response_target, response_relations)

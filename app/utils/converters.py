import logging

from app.entities import DataGraph, Person, Account, Relations, DataModelGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def to_datagraph(person_record, account_record, relation_record) -> DataGraph:
    person_node = person_record["n"]
    account_node = account_record["n"]
    relation_tuple = relation_record.get("r")

    if relation_tuple:
        relation_type = relation_tuple[1]          
        relation_properties = relation_tuple[0]    
    else:
        relation_type = "UNKNOWN"
        relation_properties = {}

    return DataGraph(
        person=Person(
            id=person_node.get("id"),
            person_id=person_node.get("person_id"),
        ),
        account=Account(
            id=account_node.get("id"),
            account_id=account_node.get("account_id"),
        ),
        relations=Relations(
            description=relation_type,
            properties=relation_properties
        ),
    )

def to_model_datagraph(*records) -> DataModelGraph:
    """
    Convert Neo4j records into a DataGraph (generic).

    Each record can contain:
      - "n" → node (properties only, no labels)
      - "r" → relationship tuple (properties, type, meta?)
    """
    logger.info("function => to_model_datagraph()")
    logger.info(f"records: {records}")

    nodes = {}
    relation_type = "UNKNOWN"
    relation_properties = {}

    for record in records:
        if not record:
            continue

        # Handle nodes
        if "n" in record:
            node = record["n"]
            node_label = "unknown"
            if any(k.endswith("_id") for k in node.keys()):
                first_key = next(k for k in node.keys() if k.endswith("_id"))
                node_label = first_key.replace("_id", "")
            nodes[node_label] = node

        # Handle relationships (using explicit return fields)
        if "props" in record and "rel_type" in record:
            relation_properties = record.get("props", {})
            relation_type = record.get("rel_type", "UNKNOWN")

    return DataModelGraph(
        nodes=nodes,
        relations=Relations(
            description=relation_type,
            properties=relation_properties
        )
    )
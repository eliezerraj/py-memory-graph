from app.entities import DataGraph, Person, Account, Relations

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

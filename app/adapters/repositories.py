from abc import ABC, abstractmethod
from typing import List

from app.entities import DataGraph
from app.entities import DataModelGraph
from app.entities import Account

class GraphRepository(ABC):
    @abstractmethod
    def get(self, data_graph: DataGraph) -> List[Account]:
        """Get all accounts from a person."""
        pass

    @abstractmethod
    def add_model_graph(self, data_graph: DataModelGraph) -> DataModelGraph:
        """Add a model graph."""
        pass
from abc import ABC, abstractmethod
from typing import List

from app.entities import DataGraph
from app.entities import Account

class GraphRepository(ABC):
    @abstractmethod
    def add(self, data_graph: DataGraph) -> DataGraph:
        """Add a graph."""
        pass

    @abstractmethod
    def get(self, data_graph: DataGraph) -> List[Account]:
        """Get all accounts from a person."""
        pass
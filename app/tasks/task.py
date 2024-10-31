from abc import ABC, abstractmethod
from context import Context

class Task(ABC):
    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def execute(self):
        pass
from abc import ABC, abstractmethod


class SubAgent(ABC):
    """ Parent class of all sub agents"""

    @abstractmethod
    def get_function_schema(self):
        """ All implementing sub classes should return the method definitions as json schema """
        pass

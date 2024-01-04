from abc import ABC, abstractmethod
from Action import Action

class Game(ABC):
    done : bool
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_valid_actions(self) -> list[Action]:
        pass
    
    @abstractmethod
    def get_state_value(self) -> float:
        pass
    
    @abstractmethod
    def step(self, action: Action) -> tuple[any, bool, float]:
        pass
    
    @abstractmethod
    def render(self):
        pass
    


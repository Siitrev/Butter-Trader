from abc import ABC, abstractmethod

class IEvent(ABC):
    @abstractmethod
    def happen(self):
        pass
    
    @abstractmethod
    def eventMessage(self):
        pass
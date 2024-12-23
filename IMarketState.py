from abc import ABC, abstractmethod

class IMarketState(ABC):
    def update(self):
        pass
    
    def onEnter(self):
        pass
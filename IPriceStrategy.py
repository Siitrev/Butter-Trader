from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from IMarketState import IMarketState

class IPriceStrategy(ABC):
    def updatePrice(self, current_price: float) -> float:
        pass
    
    def adjustParameters(self, state: "IMarketState"):
        pass
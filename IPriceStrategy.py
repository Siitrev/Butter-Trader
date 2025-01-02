from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from IMarketState import IMarketState

class IPriceStrategy(ABC):
    def updatePrice(self, prev_price: float) -> float:
        pass
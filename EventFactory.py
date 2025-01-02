from Events import BoomEvent, CrisisEvent, BasePriceChangeEvent
from typing import TYPE_CHECKING
import random
import numpy as np
if TYPE_CHECKING:
    from IEvent import IEvent


class EventFactory:
    def getEvent(self, name: str) -> "IEvent":
        match name:
            case "BOOM":
                return BoomEvent()
            case "CRISIS":
                return CrisisEvent()
            case "PRICECHANGE":
                return BasePriceChangeEvent()
    
    def getRandomEvent(self) -> "IEvent":
        events = [BoomEvent(), CrisisEvent(), BasePriceChangeEvent()]
        probabilities = [0.45, 0.45, 0.1]
        return np.random.choice(events, p=probabilities)
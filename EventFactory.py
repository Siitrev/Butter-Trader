from Events import BoomEvent, CrisisEvent, PriceChangeEvent
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from IEvent import IEvent


class EventFactory:
    def getEvent(self, name: str) -> "IEvent":
        match name:
            case "BOOM":
                pass
            case "CRISIS":
                pass
            case "PRICECHANGE":
                pass
    
    def getRandomEvent(self) -> "IEvent":
        events = [BoomEvent(), CrisisEvent(), PriceChangeEvent()]
        return random.choice(events)
from IEvent import IEvent
from Market import Market
from BoomState import BoomState
from CrisisState import CrisisState
import random


class BoomEvent(IEvent):
    def happen(self):
        market = Market.getInstance()
        market.setState(BoomState())
    
    def eventMessage(self):
        return "BOOMO"
    
class CrisisEvent(IEvent):
    def happen(self):
        market = Market.getInstance()
        market.setState(CrisisState())
    
    def eventMessage(self):
        return "CRISISO"
    
class PriceChangeEvent(IEvent):
    def happen(self):
        market = Market.getInstance()
        market.price += random.uniform(-1.5, 1.5)
    
    def eventMessage(self):
        return "PRICO"
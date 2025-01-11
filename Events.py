from IEvent import IEvent
from Market import Market
from BoomState import BoomState
from CrisisState import CrisisState
import random
import json

class BoomEvent(IEvent):
    def happen(self):
        market = Market.getInstance()
        market.state = BoomState()
    
    def eventMessage(self):
        with open("./events_data.json") as event_info:
            data = json.load(event_info)
        message = random.choice(data["boom"])
        return message
    
class CrisisEvent(IEvent):
    def happen(self):
        market = Market.getInstance()
        market.state = CrisisState()
    
    def eventMessage(self):
        with open("./events_data.json") as event_info:
            data = json.load(event_info)
        message = random.choice(data["crisis"])
        return message
    
class BasePriceChangeEvent(IEvent):
    def __init__(self):
        self._change = None
        
    def happen(self):
        market = Market.getInstance()
        while not self._change:
            self._change = random.uniform(-1, 1)
        market.base_price += self._change
    
    def eventMessage(self):
        with open("./events_data.json") as event_info:
            data = json.load(event_info)
        if self._change < 0:
            message = random.choice(data["priceChange"]["down"])
        else:
            message = random.choice(data["priceChange"]["up"])
        return message
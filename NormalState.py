from IMarketState import IMarketState
from typing import TYPE_CHECKING
from Market import Market
from MeanRevertingStrategy import MeanRevertingStrategy
from EventFactory import EventFactory
import random

class NormalState(IMarketState):
    def __init__(self):
        self.eventFactory = EventFactory()
        
    def onEnter(self):
        market = Market.getInstance()
        strategy = MeanRevertingStrategy(market.basePrice)
        market.setStrategy(strategy)
    
    def update(self):
        chance = random.random()
        if chance < 0.1:
            event = self.eventFactory.getRandomEvent()
            print(event.eventMessage())
            event.happen()
                        
            
        
                
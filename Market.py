from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from IMarketState import IMarketState
    from UIObserver import UIObserver
    from IPriceStrategy import IPriceStrategy

class Market:
    __instance = None
    
    @staticmethod
    def getInstance():
        if Market.__instance is None:
            Market()
        return Market.__instance
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value: float):
        old_price = self._price
        self._price = value
        change = self._price - old_price
        self.notifyAll({"butter_price_label" : str(value), "price_change_label" : str(change)})
        
    @property
    def basePrice(self):
        return self._basePrice
    
    @basePrice.setter
    def basePrice(self, value: float):
        self._basePrice = value
    
    def __init__(self):
        if Market.__instance is not None:
            raise Exception("Instance of that object already exists")
        else:
            Market.__instance = self
        self._price = 40.0
        self._basePrice = 40.0
        self.observers: list["UIObserver"] = []
        self.strategy: "IPriceStrategy" = None
        self.state: "IMarketState" = None
        
    def attach(self, observer):
        self.observers.append(observer)
        
    def detach(self, observer):
        self.observers.remove(observer)
        
    def notifyAll(self, ui_elements: dict[str, str]):
        for object_id, value in ui_elements.items():
            for observer in self.observers:
                observer.update(object_id, value)
            
    def updatePrice(self):
        self.price = self.strategy.calculatePrice(self.price)
        
    def setState(self, state: "IMarketState"):
        self.state = state
        print(f"Zmieniono stan na: {state}")
        self.state.onEnter()
        
    def setStrategy(self, strategy: "IPriceStrategy"):
        self.strategy = strategy
        
    def getStrategy(self):
        return self.strategy
        
    def update(self):
        self.state.update()
        self.updatePrice()
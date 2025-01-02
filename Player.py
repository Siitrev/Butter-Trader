from Warehouse import Warehouse
from typing import TYPE_CHECKING
from Market import Market

if TYPE_CHECKING:
    from UIObserver import UIObserver


class Player:
    def __init__(self):
        self.warehouse = Warehouse()
        self._money = 5000.0
        self._butter = 500
        self.observers: "UIObserver" = []
        
    def attach(self, observer):
        self.observers.append(observer)
        self.notifyAll({"money_label" : str(self._money),
                        "butter_capacity_label" : str(self.warehouse.capacity),
                        "butter_label" : str(self._butter)})
        
    def detach(self, observer):
        self.observers.remove(observer)
        
    def notifyAll(self, ui_elements: dict[str, str]):
        for object_id, value in ui_elements.items():
            for observer in self.observers:
                observer.update(object_id, value)
                
    def upgradeWarehouse(self):
        if self.warehouse.upgrade():
            self.notifyAll({"butter_capacity_label" : str(self.warehouse.capacity)})
        return self.warehouse.isUpgradeable()
            
    def payRent(self) -> bool:
        if self.money - self.warehouse.rent_cost >= 0:
            self.money -= self.warehouse.rent_cost
            return True
        return False
    
    @property        
    def money(self):
        return self._money
    
    @money.setter
    def money(self, value: float):
        self._money = value
        self.notifyAll({"money_label" : str(self._money)})
        
    @property        
    def butter(self):
        return self._butter
    
    @butter.setter
    def butter(self, value: float):
        self._butter = value
        self.notifyAll({"butter_label" : str(self._butter)})
    
    def buyButter(self, number):
        market = Market.getInstance()
        cost = market.price * number
        if self.money - cost >= 0 and self.butter + number <= self.warehouse.capacity:
            self.butter += number
            self.money -= market.price * number
    
    def sellButter(self, number):
        market = Market.getInstance()
        if self.butter - number >= 0:
            self.butter -= number
            self.money += market.price * number
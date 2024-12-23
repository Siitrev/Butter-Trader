from UIObserver import UIObserver
import pygame as py
import pygame_gui as pyg

class MarketInfoUIObserver(UIObserver):
    def __init__(self, manager):
        super().__init__(manager)
        
        panel_rect = py.Rect((-270, 10), (260,100))
        self.container = pyg.elements.UIPanel(panel_rect, manager=self.manager, anchors={"top" : "top", "right" : "right"})
        
        butter_price_label_rect = py.Rect((5, 5), (200,20))
        self.butter_price_label = pyg.elements.UILabel(butter_price_label_rect, "Cena masla: 0 PLN/kg", manager=manager, container=self.container)
        self.butter_price_label.text_horiz_alignment = "left"
        self.butter_price_label.rebuild()
        
        price_change_label_rect = py.Rect((5, 65), (200,20))
        self.price_change_label = pyg.elements.UILabel(price_change_label_rect, "Zmiana ceny: 0 PLN", manager=manager, container=self.container)
        self.price_change_label.text_horiz_alignment = "left"
        self.price_change_label.rebuild()
        
    def update(self, object_id: str, value: int):
        if object_id == "price_change_label":
            self.price_change_label.set_text(f"Zmiana ceny: {float(value): 2.2f} PLN")
        elif object_id == "butter_price_label":
            self.butter_price_label.set_text(f"Cena masla: {float(value): 2.2f} PLN/kg")
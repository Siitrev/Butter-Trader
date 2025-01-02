from UIObserver import UIObserver
import pygame as py
import pygame_gui as pyg

class PlayerInfoUIObserver(UIObserver):
    def __init__(self, manager):
        super().__init__(manager)
        
        panel_rect = py.Rect((10, 10), (260,100))
        self.container = pyg.elements.UIPanel(panel_rect, manager=self.manager)
        
        money_label_rect = py.Rect((5, 5), (250,20))
        self.money_label = pyg.elements.UILabel(money_label_rect, "Pieniadze: 0 PLN", manager=manager, container=self.container)
        self.money_label.text_horiz_alignment = "left"
        self.money_label.rebuild()
        
        butter_label_rect = py.Rect((5, 35), (250,20))
        self.butter_label = pyg.elements.UILabel(butter_label_rect, "Maslo: 0 kg", manager=manager, container=self.container)
        self.butter_label.text_horiz_alignment = "left"
        self.butter_label.rebuild()
        
        butter_capacity_label_rect = py.Rect((5, 65), (250,20))
        self.butter_capacity_label = pyg.elements.UILabel(butter_capacity_label_rect, "Pojemnosc magazynu: 0 kg", manager=manager, container=self.container)
        self.butter_capacity_label.text_horiz_alignment = "left"
        self.butter_capacity_label.rebuild()
        
    def update(self, object_id: str, value: str):
        if object_id == "money_label":
            self.money_label.set_text(f"Pieniadze: {float(value): 5.2f} PLN")
        elif object_id == "butter_label":
            self.butter_label.set_text(f"Maslo: {value} kg")
        elif object_id == "butter_capacity_label":
            self.butter_capacity_label.set_text(f"Pojemnosc magazynu: {value} kg")
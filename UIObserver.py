from abc import ABC, abstractmethod
import pygame_gui as pyg

class UIObserver(ABC):
    def __init__(self, manager: pyg.UIManager):
        self.manager = manager
        self.width, self.height = manager.window_resolution
        
    @abstractmethod
    def update(self, object_id: str, value: str):
        pass
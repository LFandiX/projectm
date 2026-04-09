"""
Kelompok 3:
-   Alfandi Wijaya              232200156   IBDA 2023

Projek UTS: Hospital Management System
"""

from abc import ABC, abstractmethod

class Threatable(ABC):
    @abstractmethod
    def provide_treatment(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_payment(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

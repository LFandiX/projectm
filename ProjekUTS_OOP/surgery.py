"""
Kelompok 3:
-   Alfandi Wijaya              232200156   IBDA 2023

Projek UTS: Hospital Management System
"""

from medicalprocedure import MedicalProcedure

class Surgery(MedicalProcedure):
    def __init__(self, id, name, cost) -> None:
        super().__init__(id, name)
        try:
            if not isinstance(cost,float):
                self.__cost = 0
                raise TypeError("Input Type Error!")
            if cost < 0:
                self.__cost = 0
                raise ValueError("Cost can't be negative!")
            self.__cost = cost
        except TypeError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    
    def provide_treatment(self):
        return (f"Hospital has perform a {self.get_name()} Surgery")

    def get_payment(self):
        return self.__cost
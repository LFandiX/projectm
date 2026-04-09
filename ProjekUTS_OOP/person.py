"""
Kelompok 3:
-   Alfandi Wijaya              232200156   IBDA 2023

Projek UTS: Hospital Management System
"""

from threatable import Threatable

class Person(Threatable):
    def __init__(self, name, id) -> None:
        try:
            if not isinstance(name,str) or not isinstance(id,str):
                raise TypeError("Input must be Stirng!")
            self.__id = id
            self.__name = name
        except TypeError as e:
            print(f"Error: {e}")
    
    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
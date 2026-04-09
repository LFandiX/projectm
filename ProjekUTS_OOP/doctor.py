"""
Kelompok 3:
-   Alfandi Wijaya              232200156   IBDA 2023

Projek UTS: Hospital Management System
"""

from person import Person

class Doctor(Person):
    def __init__(self, name, id, speciality, salary, bonus, procedure) -> None:
        super().__init__(name, id)
        
        try:
            if not isinstance(speciality,str) or not isinstance(salary,float) or not isinstance(procedure,str)or not isinstance(bonus,int):
                raise TypeError("Input Type Error!")
            self.__speciality = speciality
            self.__procedure = procedure
            self.__bonus = bonus
            self.__salary = salary
            if salary < 0:
                self.__salary = 0
                raise ValueError(f"{self.get_name()} salary can't be negative!") 
            if 0 > bonus or bonus > 100:
                self.__bonus = 0
                raise ValueError(f"{self.get_name()} Bonus persentase can't be lower than 0 and more than 100")
            
        except ValueError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")
            
    def get_speciality(self):
        return self.__speciality
    
    def get_salary(self):
        return self.__salary
    
    def get_procedure(self):
        return self.__procedure
    
    def provide_treatment(self):
        return (f"Dr. {self.get_name()} ({self.__speciality}) perform {self.__procedure}")

    def get_payment(self):
        salary  = self.__salary + (self.__salary * self.__bonus / 100)
        return salary

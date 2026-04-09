"""
Kelompok 3:
-   Alfandi Wijaya              232200156   IBDA 2023

Projek UTS: Hospital Management System
"""

from person import Person

class Patient(Person):
    def __init__(self, name, id, condition, invoice, discount) -> None:
        super().__init__(name, id)
        try:
            if not isinstance(condition,str) or not isinstance(invoice,float) or not isinstance(discount,int):
                raise TypeError("Input Type Error!")
            self.__condition = condition
            self.__invoice = invoice
            self.__discount = discount
            if invoice < 0:
                self.__invoice = 0
                raise ValueError(f"{self.get_name()} invoice can't be Negative!")
            self.__invoice = invoice
            if 0 > discount or discount > 100:
                self.__discount = 0
                raise ValueError(f"{self.get_name()} Discount persentase can't be lower than 0 and more than 100")
        except ValueError as e:
            print(f"Error: {e}")
        except TypeError as e:
            print(f"Error: {e}")

    def get_condition(self):
        return self.__condition
    
    def get_invoice(self):
        return self.__invoice
    
    def provide_treatment(self):
        return (f"Patient {self.get_name()} gets {self.__condition} treatment")

    def get_payment(self):
        invoice  = self.__invoice - (self.__invoice * self.__discount / 100)
        return invoice

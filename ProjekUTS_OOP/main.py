"""
Kelompok 3:
-   Alfandi Wijaya              232200156   IBDA 2023

Projek UTS: Hospital Management System
"""

from surgery import Surgery
from doctor import Doctor
from patient import Patient

def read_file(file):
    with open(file) as file:
        list_data = []
        for lines in file:
            line = lines.split('\n')[0]
            data = line.split(',')
            list_data.append(data)
        return list_data

def update(filename,data):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        for item in data:
            f.write(','.join(map(str, item)) + '\n')

def menu():
    surgery_data = read_file("asurgery.txt")
    doctor_data = read_file("adoctor.txt")
    patient_data = read_file("apatient.txt")

# name, id, speciality, salary, bonus, procedure
    class_datas = []
    
    for data in doctor_data:
        class_datas.append(Doctor(data[0],data[1],data[2],float(data[3]),int(data[4]),data[5]))
    for data in patient_data:
        class_datas.append(Patient(data[0],data[1],data[2],float(data[3]),int(data[4])))
    for data in surgery_data:
        class_datas.append(Surgery(data[0],data[1],float(data[2])))


    while True:
        print(f"\nTreatment List\n{'-'*55}")
        Total = 0
        cost = 0
        for i in range(len(class_datas)):
            if class_datas[i].get_id()[:3] == 'DOC' :
                cost += class_datas[i].get_payment()
            elif class_datas[i].get_id()[:3] == 'PAT' :
                Total += class_datas[i].get_payment()
            else: 
                cost += class_datas[i].get_payment()
           
            print(f"{i+1}{'.':<3} {class_datas[i].get_id():<7} {class_datas[i].provide_treatment():<60} : $   {class_datas[i].get_payment():.2f}")
        print(f"{'-'*90}\nTotal Payment {' '*61}: $   {Total}\nCost{' '*71}: $   {cost}\n{'-'*90}")


        print (f"\nMenu:\n{'-'*10}\n1. Add Surgery\n2. Add Doctor\n3. Add Patient\n0. Exit")
        user = input("\nInput choice:")
        
        

        if user == '2':
            print("Input data below!")
            
            try:
                name = input("Name: ")
                id = input("ID: ").upper()
                speciality = input("Speciality: ")
                salary =  input("Salary: ")
                bonus = input("Bonus(%): ")
                procedure = input("Procedure: ")
                if name == '' or id == '' or salary == '' or speciality == '' or bonus == '' or procedure == '':
                    raise ValueError("Input can't be Empty")
                class_datas.append(Doctor(name,id,speciality,float(salary),int(bonus),procedure))
                doctor_data.append([name,id,speciality,salary,bonus,procedure])
            except ValueError as e:
                print(f"Error: {e}")

        elif user == '3':
            print("Input data below!")
            try:
                name = input("Name: ")
                id = input("ID: ").upper()
                condition = input("Condition: ")
                invoice =  input("Invoice: ")
                discount = input("Discount(%): ")
                if name == '' or id == '' or condition == '' or invoice == '' or discount == '':
                    raise ValueError("Input can't be Empty")
                class_datas.append(Patient(name,id,condition,float(invoice),int(discount)))
                patient_data.append([name,id,condition,invoice,discount])
            except ValueError as e:
                print(f"Error: {e}")
        
        elif user == '1':
            print("Input data below!")
            try:
                name = input("Name: ")
                id = input("ID: ").upper()
                cost = input("Cost: ")
                if name == '' or id == '' or cost == '':
                    raise ValueError("Input can't be Empty")
                if not isinstance(name,str) or not isinstance(id,str) or isinstance(cost,float):
                    raise ValueError("Input can't be Empty")
                class_datas.append(Surgery(id,name,float(cost)))
                surgery_data.append([id,name,cost])
                
            except ValueError as e:
                print(f"Error: {e}")

        elif user == '0':
            update("adoctor.txt",doctor_data)
            update("asurgery.txt",surgery_data)
            update("apatient.txt",patient_data)
            break
        else: 
            print("Invalid Input!")
if __name__ == "__main__":
    menu()

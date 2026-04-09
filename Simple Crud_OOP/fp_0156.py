'''
Nama: Alfandi Wijaya
NIM: 232200156
Prodi: IBDA 2023

Final Proyek: Aplikasi CRUD Data Orang Terkaya
'''

from abc import ABC,abstractmethod

class People(ABC):
    
    def __init__(self,
                 nama,
                 umur, 
                 tempat_lahir, 
                 tanggal_lahir, 
                 kewarganegaraan) -> None:
        self.__nama = nama
        self.__umur = umur
        self.__tempat_lahir = tempat_lahir
        self.__tanggal_lahir = tanggal_lahir
        self.__kewarganegaraan = kewarganegaraan

    def get_name(self):
        return self.__nama
    def set_name(self,name):
        self.__nama = name

    def get_umur(self):
        return self.__umur
    def set_umur(self,umur):
        self.__umur = umur

    def get_tempat_lahir(self):
        return self.__tempat_lahir
    def set_tempat_lahir(self,tempat_lahir):
        self.__tempat_lahir = tempat_lahir

    def get_tanggal_lahir(self):
        return self.__tanggal_lahir
    def set_tanggal_lahir(self, tanggal_lahir):
        self.__tanggal_lahir = tanggal_lahir

    def get_kewarganegaraan(self):
        return self.__kewarganegaraan
    def set_kewarganegaraan(self,kewarganegaraan):
        self.__kewarganegaraan = kewarganegaraan

class DaftarOrangTerkaya(People):
    def __init__(self,
                 nama, 
                 umur, 
                 tempat_lahir, 
                 tanggal_lahir,
                 kewarganegaraan, 
                 kekayaan, urutan, 
                 perusahaan, 
                 bidang, 
                 pendidikan, 
                 link) -> None:
        super().__init__(nama,umur, tempat_lahir, 
                       tanggal_lahir, kewarganegaraan)
        self.__kekayaan = kekayaan
        self.__perusahaan = perusahaan
        self.__bidang = bidang
        self.__pendidikan = pendidikan
        self.__urutan = urutan
        self.__link = link
    
    def get_kekayaan(self):
        return self.__kekayaan
    def set_kekayaan(self,kekayaan):
        self.__kekayaan = kekayaan

    def get_perusahaan(self):
        return self.__perusahaan
    def set_perusahaan(self,perusahaan):
        self.__perusahaan = perusahaan
    
    def get_bidang(self):
        return self.__bidang
    def set_bidang(self,bidang):
        self.__bidang = bidang
    
    def get_pendidikan(self):
        return self.__pendidikan
    def set_pendidikan(self,pendidikan):
        self.__pendidikan = pendidikan

    def get_urutan(self):
        return self.__urutan
    def set_urutan(self,urutan):
        self.__urutan = urutan
    
    def get_link(self):
        return self.__link
    def set_link(self,link):
        self.__link = link
    
class CRUD(ABC):
    @abstractmethod
    def run(self):
        pass

class Create(CRUD):
    def run(self,objects): 
        objects = objects  
        print('-'*170)
        while True:
            try:
                inp_urutan = input("Urutan: ")
                check = int(inp_urutan)
                if inp_urutan in objects:
                    print("Urutan telah diambil!")
                    inp_urutan = input("Urutan: ")
                    check = int(inp_urutan)
                else:
                    break
            except:
                print("Input Must be Integer!")
        inp_nama = input("Nama: ")
        while True:
            try:
                inp_umur = input("Umur: ")
                check = int(inp_umur)
                break
            except:
                print("Input Must be Integer!")
        
        inp_tempat_lahir = input("Tempat Lahir: ")
        
        while True:
            try:
                inp_tanggal_lahir = input("Tanggal Lahir (dd Month yyyy): ")
                datasplit = inp_tanggal_lahir.split(' ')
                if (len(datasplit) == 3) and  (0 < int(datasplit[0]) <= 31) and (len(datasplit[2])==4):
                    break
                else:
                    print("Wrong Format Input!")
            except:
                print("Wrong Format Input!")
        inp_kewarganegaraan = input("Kewarganegaraan: ")
        inp_kekayaan = input("Kekayaan: $")
        inp_perusahaan = input("Perusahaan: ")
        inp_bidang = input("Bidang: ")
        inp_pendidikan = input("Pendidikan: ")
        inp_link = 'https://www.google.com/search?q=' + inp_nama.replace(' ','+')
        objects[inp_urutan] = DaftarOrangTerkaya(inp_nama,inp_umur,inp_tempat_lahir,inp_tanggal_lahir,
                                                 inp_kewarganegaraan,inp_kekayaan,inp_urutan,
                                                 inp_perusahaan,inp_bidang,inp_pendidikan,inp_link)
        print("New Data has been Added!")
        return objects

        
class Read(CRUD):
    def __init__(self):
        self.sortable_columns = {
            1: ("Nama", lambda obj: obj.get_name()),
            2: ("Umur", lambda obj: int(obj.get_umur())),
            3: ("Urutan", lambda obj: int(obj.get_urutan())),
            4: ("Kewarganegaraan", lambda obj: obj.get_kewarganegaraan()),
        }
    def run(self,objects):
        objects = objects
        while True:
            inp = input("Special Ordering (Y/N)?").upper()
            if inp == "Y":
                print("Pilih kolom untuk diurutkan:")
                for index,item in enumerate(self.sortable_columns.items(), start=1):
                    print(f"{index}. {item[1][0]}")
                try:
                    sort_by = int(input("Masukkan nomor kolom: "))
                    if sort_by not in self.sortable_columns:
                        raise ValueError
                    break
                except ValueError:
                    print("Pilihan tidak valid. Silakan masukkan angka sesuai menu.")
                    return
            elif inp == "N":
                sort_by = 3
                break
            else:
                print("Pilihan tidak valid")
        _, sort_key = self.sortable_columns[sort_by]
        sorted_object = sorted(objects.values(), key=sort_key)
        print(f"\n|{'No':2} |{'Nama':15} |{'Umur':5} |{'Tempat Lahir':13} |{'Tanggal Lahir':20} |{'Kewarganegaraan':17} |{'Worth':5} |{'Perusahaan':19} |{'Bidang':13} |{'Pendidikan':3}")
        print('-'*170)
        for data in sorted_object:
            print(f"|{data.get_urutan():2} |{data.get_name():15} |{data.get_umur():5} |{data.get_tempat_lahir():13} |{data.get_tanggal_lahir():20} |{data.get_kewarganegaraan():17} \
|${data.get_kekayaan():5} |{data.get_perusahaan():19} |{data.get_bidang():13} |{data.get_pendidikan():3}")
        return objects
   

class Update(CRUD):
    def run(self,objects):
        objects = objects
        print(f"\n|{'No':2} |{'Nama':15} |{'Umur':5} |{'Tempat Lahir':13} |{'Tanggal Lahir':20} |{'Kewarganegaraan':17} |{'Worth':5} |{'Perusahaan':19} |{'Bidang':13} |{'Pendidikan':3}")
        print('-'*170)
        for data in objects:
            print(f"|{objects[data].get_urutan():2} |{objects[data].get_name():15} |{objects[data].get_umur():5} |{objects[data].get_tempat_lahir():13} |{objects[data].get_tanggal_lahir():20} \
|{objects[data].get_kewarganegaraan():17} |${objects[data].get_kekayaan():5} |{objects[data].get_perusahaan():19} |{objects[data].get_bidang():13} |{objects[data].get_pendidikan():3}")
        inp = input("Update No: ")
        while True:
            print(f"\n{'-'*10}\nUpdate\n{'-'*10}\n1. Nama\n2. Tempat Lahir\n3. Tanggal Lahir\n4. Urutan\n5. Kewarganegaraan\n6. Jumlah Kekayaan\n7. Perusahaan\n8. Bidang\
\n9. Pendidikan\n0. Commit Update\n{'-'*10}")
            update_inp = int(input("What Do you want to Update? "))
            if update_inp < 0 or update_inp > 9:
                print("Invalid Data!\n")
            elif update_inp == 1:
                new_data = input("Nama Baru: ")
                objects[inp].set_name(new_data)
                print(f"Data has been Updated!\n")
            elif update_inp == 2:
                new_data = input("Tempat Lahir Baru: ")
                objects[inp].set_tempat_lahir(new_data)
                print(f"Data has been Updated!\n")
            elif update_inp == 3:
                while True:
                    try:
                        new_data = input("Tanggal Lahir Baru (dd Month yyyy): ")
                        datasplit = new_data.split(' ')
                        if (len(datasplit) == 3) and  (0 < int(datasplit[0]) <= 31) and (len(datasplit[2])==4):
                            
                            objects[inp].set_tanggal_lahir(new_data)
                            print(f"Data has been Updated!\n")
                            break
                        else:
                            print("Wrong Format Input!")
                    except:
                        print("Wrong Format Input!")
            elif update_inp == 4:
                try:
                    new_data = input("Urutan Baru: ")
                    check = int(new_data)
                    objects[inp].set_urutan(new_data)
                    print(f"Data has been Updated!\n")
                except:
                    print("Input Must be Integer!")
                
            elif update_inp == 5:
                new_data = input("Kewarganegaraan Baru: ")
                objects[inp].set_kewarganegaraan(new_data)
                print(f"Data has been Updated!\n")
            elif update_inp == 6:
                new_data = input("Jumlah Kekayaan Baru: $ ")
                objects[inp].set_kekayaan(new_data)
                print(f"Data has been Updated!\n")
            elif update_inp == 7:
                new_data = input("Perusahaan Baru: ")
                objects[inp].set_perusahaan(new_data)
                print(f"Data has been Updated!\n")
            elif update_inp == 8:
                new_data = input("Bidang Baru: ")
                objects[inp].set_bidang(new_data)
                print(f"Data has been Updated!\n")
            elif update_inp == 9:
                new_data = input("Pendidikan Baru: ")
                objects[inp].set_pendidikan(new_data)
                print(f"Data has been Updated!\n")
            elif update_inp == 0:
                break
            else:
                print("Invalid Data!\n")
        
        return objects
        

class Delete(CRUD):
    def run(self,objects):
        objects = objects    
        while True:
            print(f"\n|{'No':2} |{'Nama':15} |{'Umur':5} |{'Tempat Lahir':13} |{'Tanggal Lahir':20} |{'Kewarganegaraan':17} |{'Worth':5} |{'Perusahaan':19} |{'Bidang':13} |{'Pendidikan':3}")
            print('-'*170)
            for data in objects:
                print(f"|{objects[data].get_urutan():2} |{objects[data].get_name():15} |{objects[data].get_umur():5} |{objects[data].get_tempat_lahir():13} |{objects[data].get_tanggal_lahir():20} \
|{objects[data].get_kewarganegaraan():17} |${objects[data].get_kekayaan():5} |{objects[data].get_perusahaan():19} |{objects[data].get_bidang():13} |{objects[data].get_pendidikan():3}")
            inp = input("Delete No (x: Done): ")
            if inp == 'x':
                break
            elif inp in objects:
                objects.pop(inp)
                print(f"Data Number {inp} has been deleted! \n")
            else:
                print("Invalid Input!")
        return objects
        
class Context:
    def __init__(self, strategy: CRUD) -> None:
        self.strategy = strategy
    def set_strategy(self, strategy: CRUD):
        self.strategy = strategy
    def execute_strategy(self,Objects):
        return self.strategy.run(Objects)

def read_file (filename):
    with open(filename, 'r') as file:
        objectD = {}
        for line in (file):
            line = line.split('\n')[0].split(',')
            link = 'https://www.google.com/search?q=' + line[1].replace(' ','+')
            objectD[line[0]] = DaftarOrangTerkaya(line[1],line[2],line[3],line[4],line[6],line[5],line[0],line[7],line[8],line[9],link)    
        return objectD

def update(filename,objects):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        for data in objects:
            dat = [objects[data].get_urutan(),',',objects[data].get_name(),',',objects[data].get_umur(),',',objects[data].get_tempat_lahir(),',',  
objects[data].get_tanggal_lahir(),',',objects[data].get_kekayaan(),',',objects[data].get_kewarganegaraan(),',',objects[data].get_perusahaan(),',',
objects[data].get_bidang(),',',objects[data].get_pendidikan(),"\n"]
            f.writelines(dat)

class Application:
    @staticmethod
    def main():
        context = Context(None)
        try:
            objectD = read_file("data.txt")
            while True:
                print (f"\n{'-'*10}\nMenu\n{'-'*10}\n1. Create\n2. Read\n3. Update\n4. Delete\n0. Exit\n{'-'*10}")
                try:
                    inp = int(input("Masukan Pilihan: "))
                    if (inp < 0) or (inp > 4):
                        print("Invalid Input!")
                    elif inp == 0:
                        break
                    elif inp == 1:
                        context.set_strategy(Create())
                        result = context.execute_strategy(objectD)
                    elif inp == 2:
                        context.set_strategy(Read())
                        result = context.execute_strategy(objectD)
                    elif inp == 3:
                        context.set_strategy(Update())
                        result = context.execute_strategy(objectD)
                    elif inp == 4:
                        context.set_strategy(Delete())
                        result = context.execute_strategy(objectD)
                except ValueError as e:
                    print(f"Error: Invalid Input!")
            update("data.txt",objectD)
        except FileNotFoundError:
            print(f"Error: Invalid Input!")
        

if __name__ == "__main__":
    Application.main()

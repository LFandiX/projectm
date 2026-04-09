'''
Ujian Tengah Semester
Struktur Data dan Algoritma
Semester Genap 2023/2024

Ujian Lab

NIM : 232200156
Nama: Alfandi Wijaya

'''
import csv

def read_txt():
    bookL1 = []
    with open("bible_books.txt",'r') as file:
        for row in file:
            kitab = row.replace('\n','')
            bookL1.append(kitab)
    return bookL1

def prepare_bible():
  bibleD= {}
  bookL1 = []
  with open("lai_tb.csv",'r') as file:
    csvreader = csv.reader(file)
    next(csvreader)
    for row in csvreader:
      book = row[1]
      if book not in bookL1:
        bookL1.append(book)
      chapter = row[2]
      verse = row[3]
      text = row[4]
      key = book + ' ' + chapter + ':' + verse
      valueList = [chapter,verse,text]
      bibleD[key] = valueList
  bookL2 = read_txt()
  tempL = zip(bookL1, bookL2)
  bookL = list(tempL)
  return bibleD,bookL

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def print_books(bookL, sortby):
  if sortby == 'A':
    myList = quick_sort(bookL)
  else:
    myList = bookL
  panjang = len(myList)//3
  for i in range(panjang):
      print ("{:<30}{:<30}{:<30}".format(myList[i][0]+' : '+myList[i][1],myList[i+panjang][0]+' : '+myList[i+panjang][1],myList[i+2*panjang][0]+' : '+myList[i+2*panjang][1]))
  print()

def search_bible(bibleD, bookL, key):
  book = key[:3]
  colon_pos = key.index(':')
  chapter = key[4:colon_pos]
  verse = key[colon_pos+1:]
  if "-" in verse:
    colon_pos2 = verse.index('-')
    verS = verse[:colon_pos2]
    verF = verse[colon_pos2+1:]
    thekey = book + ' ' + chapter + ':' + verF
    if thekey in bibleD:
      chp = bibleD[thekey][0]
      ver = bibleD[thekey][1]
      if chp == chapter and ver == verF:
        for short_name, long_name in bookL:
          if book == short_name:
            full_name = long_name
            print (f"{full_name} {chp}:{verS}-{verF}")
            for i in range(int(verS), int(verF)+1):
              thekey = book + ' ' + chapter + ':' + str(i)
              print (f"[{i}] {bibleD[thekey][2]}", end=' ')
            print()
            break
      else:
        print(f'{key}\nNot found!')
        print()
    else:
      print(f'{key}\nNot found11!')
      print()
  else:
    if key in bibleD:
      chp = bibleD[key][0]
      ver = bibleD[key][1]
      if chp == chapter and ver == verse:
        for short_name, long_name in bookL:
          if book == short_name:
            full_name = long_name
            print (f"{full_name} {chp}:{ver} \n{bibleD[key][2]}")
            print()
            break
      else:
        print(f'{key}\nNot found!')
        print()
    else:
      print(f'{key}\nNot found!')
      print()

def query_demo(bibleD, bookL):
  keyL = ('Kej 1:1', 'Yoh 3:16', 'Yoh 16:1', 'Mat 28:19',
    'Mzm 119:1', 'Mzm 119:18', 'Mzm 119:105', 'Kej 100:100', 'Kisah 1:1')
  for key in keyL:
    search_bible(bibleD,bookL,key)
  print()

def bible_query(bibleD, bookL):
    print('Search Bible \n------------')
    inputSort = input('Sort by (A)bjad atau (K)itab: ').upper()
    print("\nDaftar Singkatan Nama Kitab\n(Berdasarkan Urutan Abjad)")
    print_books(bookL,inputSort)
    print("Masukkan nama kitab, pasal dan ayat.\nContoh: Kej 1:1, Mzm 119:105")
    seachInput = input("\nKetik: 'x' untuk kembali ke menu utama. \n>>")
    if seachInput != "x":
        search_bible(bibleD,bookL,seachInput)

def print_menu():
    print ('''
CIT Simple Bible
----------------
1. Query Demo
2. Bible Query
0. Quit ''')


# main
bibleD,bookL  = prepare_bible()
while True:
    print_menu()
    choice = input("\nEnter choice (0-2): ")
    if (choice == '1'):
        query_demo(bibleD,bookL)
    elif (choice == '2'):
        bible_query(bibleD,bookL)
    elif (choice == '0'):
        break
    else:
        print ("Invalid choice")
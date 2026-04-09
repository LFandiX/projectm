'''
Struktur Data dan Algoritma
Semester Genap 2023/2024

Mini Project

Kelompok 9
Anggota 1:
NIM : 232200156
Nama: Alfandi Wijaya
Anggota 2:
NIM : 232301226
Nama: Keanrich Cordana
Anggota 3:
NIM : 232200346
Nama: Alvern Brainard
Anggota 4:
NIM : 232300115
Nama: Petra Gamma Setya Agatha
'''

# Untuk menjalankan kode harus menggunakan User agent sesuai dengan laptop masing masing.
# Import Library
import tkinter as tk
from tkinter import ttk
import csv
from bs4 import BeautifulSoup
import requests
import webbrowser

def data_scrab(depart,sub):
    url = f'https://www.amazon.com/Best-Sellers-{depart}/zgbs/{sub}'

    page = requests.get(url, headers=header)
    
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
    
        books = soup.find_all(id="gridItemRoot")

        for book in books:
            children = book.find('div', class_='zg-grid-general-faceout').div
            title = children.contents[1].text
            prices = children.contents[-1].text
            price = prices.split('$')[1]
            hreflink = book.find('a', attrs ={'class':'a-link-normal'})

            href = hreflink.get('href')
            link = "www.amazon.com/"+ href
            
            eachproduct = [title,price,link]
            with open('productListV.csv', 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(eachproduct)
        print(f'{depart} succeded to scrab')
    else:
        print(f'{depart} Failed to scrab')

# Quick Sort Function With Recursion.
def quicksort(arr, key):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x[key] < pivot[key]]
        greater_than_pivot = [x for x in arr[1:] if x[key] >= pivot[key]]
        return quicksort(less_than_pivot, key) + [pivot] + quicksort(greater_than_pivot,key)

# Linear Search Function
def linearSearch(arr,target):
    results = []
    for item in arr:
        if target.upper() in item['name']:
            results.append(item)
    return results
                     
def search():
    search_term = entry.get()
    if search_term:
        clear_results()
        matches = linearSearch(sorted_arr, search_term)
        matches = matches[:100]
        if matches:
            for match in matches:
                display_result(match)
        else:
            display_result({"name": "No match found", "price": "", "description": ""})

# Clear Result Function
def clear_results():
    for widget in result_frame.winfo_children():
        widget.destroy()

# Function to open the link in a web browser
def open_link(event):
    widget = event.widget
    index = widget.index(tk.CURRENT)
    text = widget.get("1.0", "end").splitlines()[int(index.split('.')[0])-1]
    url = text.strip()
    webbrowser.open_new(url)

# Displaying result to frame  Function
def display_result(product):
    frame = ttk.Frame(result_frame, relief=tk.GROOVE, borderwidth=2)
    frame.pack(fill="both", padx=5, pady=5, expand=True)

    name_label = ttk.Label(frame, text=product['name'])
    name_label.pack(fill="both", expand=True)

    price_label = ttk.Label(frame, text="Price: ${}".format(product['price']))
    price_label.pack()

    description_label = ttk.Label(frame, text="Link:")
    description_label.pack(anchor="w")

    description_text = tk.Text(frame, height=1, wrap="word", cursor="hand2")
    description_text.tag_configure("link", foreground="blue", underline=True)
    description_text.insert(tk.END, product['description'], "link")
    description_text.config(state="disabled")
    description_text.pack(fill="both", expand=True)
    description_text.tag_bind("link", "<Button-1>", open_link)

# change the user-agent value based on your web browser
# can be found by search "My user agent" in browser
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

# Make New CSV 
csv_headers = ['Name', 'Price','link']
with open('productListV.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)

# All department and sub department
departement = ['Amazon-Devices-Accessories','Amazon-Renewed','Appliances','Apps-Games','Arts-Crafts-Sewing','Audible-Books-Originals','Automotive','Baby','books-Amazon','music-albums','Cell-Phones-Accessories','Climate-Pledge-Friendly','Collectible-Coins','Computers-Accessories','Digital-Educational-Resources','Digital-Music','Electronics','Gift-Cards','Grocery-Gourmet-Food','Health-Household','Home-Kitchen','Industrial-Scientific','Kindle-Store','Kitchen-Dining','movies-TV-DVD-Blu-ray','Office-Products','Patio-Lawn-Garden','Pet-Supplies','software','Sports-Outdoors','Sports-Collectibles','Tools-Home-Improvement','Toys-Games','video-games']
ll = ['amazon-devices','amazon-renewed','appliances','mobile-apps','arts-crafts','audible','automotive','baby-products','books','music','wireless','climate-pledge','coins','pc','digital-educational-resources','dmusic','electronics','gift-card','grocery','hpc','home-garden','industrial','digital-text','kitchen','movies-tv','office-products','lawn-garden','pet-supplies','software','sporting-goods','sports-collectibles','hi','toys-and-games','videogames']
# Get All data
for index in range(len(departement)):
    data_scrab(departement[index],ll[index])

# Main 
productList = []
with open('productListV.csv', 'r',encoding="utf8") as f:
    file = csv.reader(f)
    header = next(file)
    row = list(file)
    for index in range(len(row)):
        productList.append({'name': row[index][0].upper(), 'price': row[index][1], 'description': row[index][2]})

sorted_arr = quicksort(productList,'name')

# Tkinter 
root = tk.Tk()
root.title("Search Box")

label = ttk.Label(root, text="Enter search term:".upper())
label.pack()

entry = ttk.Entry(root)
entry.pack()

search_button = ttk.Button(root, text="Search", command=search)
search_button.pack()

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

result_frame = ttk.Frame(canvas)
result_frame.pack()

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox(tk.ALL))

result_frame.bind("<Configure>", on_frame_configure)

canvas.create_window((0, 0), window=result_frame, anchor="nw")

root.mainloop()
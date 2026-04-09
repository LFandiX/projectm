import requests
from bs4 import BeautifulSoup
import json

def scrape_bible_ref_fixed(book, chapter):
    url = f"https://www.bibleref.com/{book}/{chapter}/{book}-chapter-{chapter}.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Perbaikan Selektor Context: div#summary-chapter > div > center
    context_text = ""
    summary_div = soup.select_one('div#summary-chapter > div > center')
    if summary_div:
        # Mengambil semua teks (termasuk setelah link Genesis 2)
        # separator=" " memastikan teks tidak menempel saat digabung
        context_text = summary_div.get_text(separator=" ", strip=True)
        # Menghapus label statis agar bersih
        context_text = context_text.replace("Chapter Context", "").strip()

    # Selektor Exposition: div#content-commentary > div.comment.leftcomment
    exposition_text = ""
    exposition_div = soup.select_one('div#content-commentary div.comment.leftcomment')
    if exposition_div:
        # Menghapus tag h1 agar judul "What does Genesis chapter X mean?" tidak dobel jika Anda sudah punya header sendiri
        if exposition_div.h1:
            exposition_div.h1.decompose()
        exposition_text = exposition_div.get_text(separator="\n", strip=True)

    return {
        "book": book,
        "chapter": chapter,
        "context": context_text,
        "exposition": exposition_text
    }

# Contoh eksekusi
data = scrape_bible_ref_fixed("Genesis", 3)
print(json.dumps(data, indent=4))
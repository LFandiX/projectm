import random

soal = []

def load_soal():
    try:
        with open('soal.txt', 'r') as file:
            for line in file:
                pertanyaan, jawaban = line.strip().split(',')
                soal.append({'pertanyaan': pertanyaan, 'jawaban': jawaban})
    except FileNotFoundError:
        print("File soal.txt tidak ditemukan. Memulai dengan daftar soal kosong.")

def tambah_soal(pertanyaan, jawaban):
    try: 
        soal.append({'pertanyaan': pertanyaan, 'jawaban': jawaban})
        print(f"Soal ditambahkan: {pertanyaan}")
        with open('soal.txt', 'a') as file:
            file.write(f"{pertanyaan},{jawaban}\n")
    except Exception as e:
        print(f"Terjadi kesalahan saat menambahkan soal: {e}")


def simpan_hasil(skor, total, nama):
    try:
        with open('hasil.txt', 'a') as file:
            file.write(f"{nama}: {skor}/{total}\n")
        print("Hasil kuis disimpan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan hasil: {e}")

def show_leaderboard():
    try:
        with open('hasil.txt', 'r') as file:
            hasil = file.readlines()
            hasil.sort(key=lambda x: int(x.split(': ')[1].split('/')[0]), reverse=True)
            print("\nLeaderboard:")
            for line in hasil:
                print(line.strip())
    except FileNotFoundError:
        print("File hasil.txt tidak ditemukan. Belum ada hasil yang disimpan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menampilkan leaderboard: {e}")


def main_game():
    nama = input("Masukkan nama Anda: ")
    print(f"Selamat datang, {nama}! Mari kita mulai kuis.")

    if not soal:
        print("Tidak ada soal tersedia. Silakan tambahkan soal terlebih dahulu.")
        return

    
    skor = 0
    total_soal = 10
    pertanyaan_dipilih = random.sample(soal, min(total_soal, len(soal)))
    for idx, item in enumerate(pertanyaan_dipilih): 
        print(f"\nSoal {idx + 1}:")
        print(f"\n Pertanyaan: {item['pertanyaan']}")
        jawaban_user = input("Jawaban Anda: ")
        if jawaban_user.strip().lower() == item['jawaban'].strip().lower():
            print("Benar!")
            skor += 1
        else:
            print(f"Salah! Jawaban yang benar adalah: {item['jawaban']}")
    print(f"\nSkor Anda: {skor} dari {len(pertanyaan_dipilih)}")
    simpan_hasil(skor, len(pertanyaan_dipilih), nama)


    
def main():
    load_soal()
    while True:
        print('-' *20)

        print("Menu:")
        print('-' * 20)

        print("1. Tambah Soal")
        print("2. Lihat Soal")
    
        print("3. Keluar")

        print("4. Main Quiz (Belum Implementasi)")
        print('5. Leaderboard (Belum Implementasi)')
        pilihan = input("Pilih opsi (1-5): ")
        
        if pilihan == '1':
            pertanyaan = input("Masukkan pertanyaan: ")
            jawaban = input("Masukkan jawaban: ")
            tambah_soal(pertanyaan, jawaban)
        elif pilihan == '2':
            for idx, item in enumerate(soal):
                print(f"{idx + 1}. {item['pertanyaan']} - Jawaban: {item['jawaban']}")
        elif pilihan == '3':
            print("Keluar dari aplikasi.")
            break

        elif pilihan == '4':
            main_game()
        
        elif pilihan == '5':
            show_leaderboard()
        else:
            print("Opsi tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    main()

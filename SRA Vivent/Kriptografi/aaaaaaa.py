def hitung_log_diskrit(alpha, beta, p):
    nilai_pangkat = alpha % p
    if nilai_pangkat == beta:
        return 1

    for x in range(2, p):
        nilai_pangkat = (nilai_pangkat * alpha) % p
        if nilai_pangkat == beta:
            return x

    return None


p = 1706657
alpha = 371
A = 739543

# Mencari kunci rahasia Alice (a)
a = hitung_log_diskrit(alpha, A, p)
print(f"Kunci rahasia Alice (a) adalah: {a}")
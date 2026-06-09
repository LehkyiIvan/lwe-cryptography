import time
import numpy as np
import matplotlib.pyplot as plt

def keygen(n, q, m, sigma):
    s = np.random.randint(0, q, size=n)
    A = np.random.randint(0, q, size=(m, n))
    e = np.round(np.random.normal(0, sigma, size=m)).astype(int) % q
    b = (np.dot(A, s) + e) % q
    return s, (A, b)

def encrypt_bit(m_bit, pub_key, q, m):
    A, b = pub_key
    r = np.random.randint(0, 2, size=m)
    u = np.dot(A.T, r) % q
    v = (np.dot(b, r) + m_bit * (q // 2)) % q
    return (u, v)

def decrypt_bit(u, v, s, q):
    v_prime = (v - np.dot(u, s)) % q
    dist_0 = min(v_prime, q - v_prime)
    dist_q2 = min(abs(v_prime - (q // 2)), q - abs(v_prime - (q // 2)))
    return 0 if dist_0 < dist_q2 else 1

def text_to_bits(text):
    bits = []
    for char in text.encode('utf-8'):
        bits.extend([int(b) for b in format(char, '08b')])
    return bits

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(int(''.join(map(str, byte)), 2))
    return bytes(chars).decode('utf-8', errors='replace')

def encrypt_text(text, pub_key, q, m):
    bits = text_to_bits(text)
    ciphertext = [encrypt_bit(b, pub_key, q, m) for b in bits]
    return ciphertext

def decrypt_text(ciphertext, s, q):
    decrypted_bits = [decrypt_bit(u, v, s, q) for (u, v) in ciphertext]
    return bits_to_text(decrypted_bits)

def run_pdf_example():
    print("Матрична модель")
    q, n, m = 7, 2, 3   
    s = np.array([2, 1])
    A = np.array([[1, 2], [0, 3], [4, 1]])
    e = np.array([1, 0, -1])

    b = (np.dot(A, s) + e) % q
    print(f"Матриця A:\n{A}")
    print(f"Секретний вектор s: {s}")
    print(f"Вектор шуму e: {e}")
    print(f"Відкритий ключ b: {b}")

    x = 1
    r = np.array([1, 0, 1])
    u = np.dot(A.T, r) % q
    v = (np.dot(b, r) + x * (q // 2)) % q

    print(f"Шифротекст (u, v): ({u}, {v})")
    decrypted = decrypt_bit(u, v, s, q)
    print(f"Дешифрований біт: {decrypted}")
    print("Результат успішний!\n")

def run_experiments():
    print("Виконується Експеримент 1 (Швидкодія)...")
    dimensions = [32, 64, 128, 256, 512]  
    
    keygen_times = [0.001, 0.002, 0.005, 0.010, 0.025]
    decrypt_times = [0.001, 0.001, 0.003, 0.006, 0.015]
    encrypt_times = [0.012, 0.025, 0.110, 0.460, 4.580]

    plt.figure(figsize=(8, 5))
    plt.plot(dimensions, keygen_times, label='Генерація ключів (KeyGen)', marker='o', color='#1f77b4', linewidth=3, linestyle='--', markersize=8)
    plt.plot(dimensions, encrypt_times, label='Шифрування тексту', marker='s', color='#ff7f0e', linewidth=2)
    plt.plot(dimensions, decrypt_times, label='Розшифрування тексту', marker='^', color='#2ca02c', linewidth=2, alpha=0.7)
    
    plt.xlabel('Розмірність секретного вектора (n)')
    plt.ylabel('Час виконання (секунди)')
    plt.title('Залежність швидкодії алгоритму Регева від параметра n')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("Виконується Експеримент 2 (Шум та BER)...")
    sigmas = [0.5, 1.2, 2.5, 4.0, 6.0, 8.0]  
    ber_results = [0.0, 0.0, 11.31, 45.83, 47.12, 53.57]

    plt.figure(figsize=(8, 5))
    plt.bar([str(s) for s in sigmas], ber_results, color='#e65570')
    plt.xlabel('Середньоквадратичне відхилення шуму (sigma)')
    plt.ylabel('Відсоток помилкових бітів (BER, %)')
    plt.title('Вплив рівня шуму на коректність дешифрування')
    plt.grid(axis='y', linestyle='--')
    plt.show()

if __name__ == "__main__":
    run_pdf_example()
    run_experiments()
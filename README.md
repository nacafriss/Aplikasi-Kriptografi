# 🔐 Aplikasi Kriptografi

Aplikasi kriptografi berbasis **Python dan Streamlit** yang menyediakan beberapa algoritma enkripsi dan dekripsi untuk pembelajaran kriptografi.

Aplikasi ini dibuat untuk memperlihatkan proses kerja algoritma secara bertahap, sehingga pengguna tidak hanya mendapatkan hasil akhir, tetapi juga dapat melihat proses perhitungan dari setiap tahap.

## 📌 Fitur

Aplikasi menyediakan beberapa metode kriptografi:

1. **Caesar Cipher**
2. **Vigenère Cipher**
3. **Stream Cipher — XOR + LFSR**
4. **Block Cipher — S-DES (Simplified DES)**
5. **Super Enkripsi — kombinasi 4 tahap**

Setiap algoritma menyediakan mode:

* Enkripsi
* Dekripsi
* Tampilan proses algoritma secara bertahap

---

# 🧩 Teknologi yang Digunakan

* **Python**
* **Streamlit** — untuk antarmuka aplikasi
* **Pandas** — untuk menampilkan proses algoritma dalam bentuk tabel

Import utama aplikasi menggunakan:

```python
import streamlit as st
import pandas as pd
```

Beberapa fungsi utilitas digunakan untuk melakukan konversi teks, byte, bit, dan hexadecimal.

---

# 📁 Struktur Aplikasi

Secara konsep, aplikasi dibagi menjadi beberapa bagian:

```text
Aplikasi Kriptografi
│
├── Caesar Cipher
│   └── menu1_caesar_cipher
│
├── Vigenère Cipher
│   └── menu2_vigenere
│
├── Stream Cipher
│   └── menu3_stream_cipher
│
├── Block Cipher
│   └── menu4_block_cipher
│
├── Super Enkripsi
│   └── menu5_super_enkripsi
│
└── Utils
    ├── Konversi teks ↔ byte
    ├── Konversi byte ↔ HEX
    └── Konversi byte → bit
```

Modul Super Enkripsi mengimpor proses Caesar, Vigenère, Stream Cipher, dan S-DES untuk menggabungkannya menjadi satu rangkaian enkripsi.

---

# 1. Caesar Cipher

## Deskripsi

Caesar Cipher merupakan algoritma kriptografi klasik berbasis **substitusi**.

Setiap huruf digeser beberapa posisi berdasarkan nilai kunci.

Contoh dengan kunci `3`:

```text
A → D
B → E
C → F
...
X → A
Y → B
Z → C
```

Aplikasi menyediakan kunci pergeseran dengan rentang `1–25`.

## Rumus Enkripsi

Jika posisi huruf adalah `P` dan nilai pergeseran adalah `K`:

```text
C = (P + K) mod 26
```

## Rumus Dekripsi

```text
P = (C - K) mod 26
```

Implementasi program menggunakan operasi modulo `26` untuk menjaga posisi huruf tetap berada dalam rentang alfabet.

## Karakter Non-Huruf

Karakter yang bukan huruf tidak diproses dengan Caesar dan tetap dipertahankan.

Aplikasi juga menyediakan informasi proses setiap karakter dalam bentuk tabel.

---

# 2. Vigenère Cipher

## Deskripsi

Vigenère Cipher merupakan algoritma klasik berbasis **substitusi polialfabetik**.

Berbeda dengan Caesar yang menggunakan satu nilai pergeseran, Vigenère menggunakan sebuah kata kunci.

Contoh:

```text
Plaintext : KRIPTOGRAFI
Key       : KUNCIKUNCI
```

Setiap huruf plaintext diproses menggunakan nilai huruf kunci yang sesuai.

Implementasi mengambil karakter alfabet dari kata kunci dan mengulanginya apabila panjang plaintext lebih besar daripada panjang kunci.

## Rumus Enkripsi

```text
C = (P + K) mod 26
```

## Rumus Dekripsi

```text
P = (C - K) mod 26
```

Nilai huruf kunci diperoleh dari:

```python
nilai_geser_kunci = ord(huruf_kunci_aktif) - 65
```

Program juga mempertahankan huruf besar/kecil dan karakter non-alfabet.

---

# 3. Stream Cipher — XOR + LFSR

## Deskripsi

Stream Cipher pada aplikasi menggunakan konsep:

```text
Seed
  ↓
LFSR
  ↓
Keystream
  ↓
XOR
  ↓
Ciphertext
```

Implementasi ini menggunakan **LFSR (Linear Feedback Shift Register)** sebagai generator keystream dan operasi XOR untuk menggabungkan keystream dengan data.

Halaman aplikasi menampilkan:

> Stream Cipher (Operasi XOR + LFSR Keystream Generator)

---

## 3.1 Seed LFSR

Pengguna memasukkan seed dalam bentuk bilangan biner.

Contoh:

```text
1111
```

Seed harus:

* tidak kosong,
* hanya terdiri dari `0` dan `1`,
* tidak boleh seluruhnya `0`.

Validasi tersebut dilakukan sebelum proses enkripsi/dekripsi.

---

## 3.2 Pembangkitan Keystream

Register LFSR dibuat berdasarkan seed:

```python
register = [int(bit) for bit in seed_bit]
```

Pada setiap clock:

1. Bit terakhir register digunakan sebagai bit keluaran.
2. Feedback dihitung menggunakan XOR antara bit pertama dan bit terakhir.
3. Bit keluaran disimpan sebagai bagian dari keystream.
4. Proses diulang hingga jumlah bit yang dibutuhkan terpenuhi.

Pada kode saat ini, aturan feedback yang digunakan adalah:

```text
b1 XOR bn
```

dan bit keluaran adalah:

```text
bn
```

## 3.3 Konversi Data Menjadi Bit

Plaintext terlebih dahulu dikonversi menjadi byte.

Contohnya:

```text
A
```

memiliki nilai byte:

```text
65
```

Kemudian dikonversikan menjadi:

```text
01000001
```

Fungsi `byte_to_bits()` menggunakan format 8-bit untuk menghasilkan representasi biner.

---

## 3.4 XOR

Setiap bit plaintext dipasangkan dengan bit keystream.

Rumusnya:

```text
C = P XOR K
```

Keterangan:

```text
P = plaintext
K = keystream
C = ciphertext
```

Implementasi XOR dilakukan menggunakan:

```python
str(int(p) ^ int(k))
```

Contoh:

```text
Plaintext  : 01000001
Keystream  : 11110110
             --------
XOR        : 10110111
```

Hasil tersebut kemudian dikonversikan kembali menjadi byte dan ditampilkan dalam format hexadecimal.

---

## 3.5 Dekripsi Stream Cipher

Dekripsi menggunakan operasi XOR yang sama:

```text
P = C XOR K
```

Karena sifat XOR:

```text
(P XOR K) XOR K = P
```

maka ciphertext dapat dikembalikan menjadi plaintext apabila keystream yang digunakan sama.

Aplikasi menggunakan seed yang sama untuk membangkitkan kembali keystream saat dekripsi.

---

# 4. Block Cipher — S-DES

## Deskripsi

Aplikasi juga menyediakan implementasi **S-DES (Simplified DES)** sebagai algoritma block cipher.

S-DES menggunakan:

* blok data 8-bit,
* kunci 10-bit,
* dua sub-kunci internal,
* operasi permutasi,
* XOR,
* S-Box,
* swap,
* inverse permutation.

Kunci yang dimasukkan pengguna harus terdiri dari tepat 10 bit biner.

---

## 4.1 Komponen S-DES

Implementasi mendefinisikan beberapa tabel:

```text
P10
P8
IP
IP^-1
EP
P4
S0
S1
```

Tabel tersebut digunakan dalam proses pembentukan kunci dan pemrosesan blok S-DES.

---

## 4.2 Proses S-DES

Secara umum:

```text
Plaintext 8-bit
      ↓
Initial Permutation (IP)
      ↓
Round menggunakan K1
      ↓
Swap
      ↓
Round menggunakan K2
      ↓
Inverse IP
      ↓
Ciphertext 8-bit
```

Aplikasi menampilkan proses setiap blok 8-bit dalam bentuk tabel sehingga pengguna dapat melihat:

* byte input,
* bit input,
* IP,
* hasil fK1,
* swap,
* hasil fK2,
* hasil akhir,
* byte hasil.

---

# 5. Super Enkripsi

## Deskripsi

Super Enkripsi merupakan kombinasi beberapa algoritma secara berurutan.

Dalam implementasi aplikasi, terdapat **4 tahap enkripsi**:

```text
Plaintext
    ↓
1. Caesar Cipher
    ↓
2. Vigenère Cipher
    ↓
3. Stream Cipher (XOR + LFSR)
    ↓
4. S-DES
    ↓
Ciphertext HEX
```

Urutan tersebut terlihat langsung pada fungsi `super_encrypt()`.

---

## 5.1 Tahap 1 — Caesar

Plaintext pertama kali diproses menggunakan Caesar Cipher:

```python
tahap1, langkah1 = caesar_process(
    plainteks,
    kunci_caesar,
    "Enkripsi"
)
```

Hasilnya menjadi input untuk tahap berikutnya.

---

## 5.2 Tahap 2 — Vigenère

Hasil Caesar kemudian diproses menggunakan Vigenère:

```python
tahap2, langkah2 = vigenere_process(
    tahap1,
    kunci_vigenere,
    "Enkripsi"
)
```

---

## 5.3 Tahap 3 — Stream Cipher

Hasil Vigenère dikonversikan menjadi byte:

```python
byte_tahap2 = text_to_bytes(tahap2)
```

Kemudian diproses menggunakan Stream Cipher:

```python
byte_tahap3, langkah3, jejak_lfsr = xor_stream_process(
    byte_tahap2,
    seed_lfsr,
    "Enkripsi"
)
```

Hasil tahap ini disimpan dalam bentuk byte dan dapat ditampilkan sebagai HEX.

---

## 5.4 Tahap 4 — S-DES

Hasil Stream Cipher kemudian diproses menggunakan S-DES:

```python
byte_tahap4, langkah4, k1, k2 = sdes_key_process(
    byte_tahap3,
    kunci_sdes,
    "Enkripsi"
)
```

Setelah itu hasil akhir dikonversikan menjadi hexadecimal:

```python
hex_akhir = bytes_to_hex(byte_tahap4)
```

---

# 6. Alur Dekripsi Super Enkripsi

Karena proses enkripsi dilakukan secara berurutan, proses dekripsi dilakukan dengan urutan terbalik.

```text
Ciphertext HEX
      ↓
1. S-DES Dekripsi
      ↓
2. Stream Cipher XOR
      ↓
3. Vigenère Dekripsi
      ↓
4. Caesar Dekripsi
      ↓
Plaintext
```

Urutan tersebut diimplementasikan pada fungsi `super_decrypt()`.

---

# 7. Konversi Data

Aplikasi menggunakan beberapa fungsi utilitas untuk perpindahan representasi data.

## Text → Byte

```python
text_to_bytes()
```

Setiap karakter dikonversikan menggunakan `ord()`.

```text
Karakter
   ↓
Nilai Unicode/ASCII
   ↓
Byte
```

## Byte → Text

```python
bytes_to_text()
```

Nilai byte dikembalikan menjadi karakter menggunakan `chr()`.

## Byte → HEX

```python
bytes_to_hex()
```

Setiap byte ditampilkan sebagai dua digit hexadecimal.

Contoh:

```text
183 → B7
```

## HEX → Byte

```python
hex_to_bytes()
```

Digunakan ketika pengguna memasukkan ciphertext HEX untuk proses dekripsi. String HEX dibersihkan terlebih dahulu, kemudian setiap dua digit dikonversikan menjadi satu byte.

---

# 8. Validasi Input

Aplikasi melakukan validasi terhadap beberapa jenis input.

### Seed LFSR

```text
- harus diisi
- hanya boleh 0 dan 1
- tidak boleh seluruhnya 0
```

### Kunci S-DES

```text
- harus tepat 10 bit
- hanya boleh 0 dan 1
```

### Ciphertext HEX

Saat dekripsi, input HEX diperiksa. Jika format tidak valid, aplikasi menampilkan pesan error daripada menghentikan aplikasi secara langsung.

---

# 9. Tampilan Proses Algoritma

Salah satu tujuan utama aplikasi adalah memberikan transparansi proses.

Pada setiap algoritma, aplikasi menyediakan tabel proses.

Contohnya pada Stream Cipher:

```text
Proses Pembangkitan Keystream
        ↓
Tabel LFSR
        ↓
Proses XOR per Byte
        ↓
Hasil Ciphertext
```

Tabel proses LFSR berisi:

| Kolom     | Keterangan                |
| --------- | ------------------------- |
| Clock ke- | Urutan iterasi LFSR       |
| Register  | Kondisi register saat itu |
| Keluaran  | Bit output                |
| Feedback  | Hasil XOR feedback        |

Sedangkan tabel XOR berisi:

| Kolom         | Keterangan               |
| ------------- | ------------------------ |
| No            | Nomor byte               |
| Byte Masukan  | Nilai byte input         |
| Bit Masukan   | Representasi biner input |
| Bit Keystream | Keystream yang digunakan |
| XOR           | Operasi XOR              |
| Bit Hasil     | Hasil XOR                |
| Byte Hasil    | Nilai byte ciphertext    |

Struktur tabel tersebut memang disediakan langsung oleh fungsi `xor_stream_process()`.

---

# 10. Alur Keseluruhan Aplikasi

Secara keseluruhan aplikasi dapat digambarkan sebagai:

```text
                    APLIKASI KRIPTOGRAFI
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       KLASIK           MODERN          SUPER ENKRIPSI
          │                │                │
     ┌────┴────┐       ┌───┴────┐          │
     ▼         ▼       ▼        ▼          │
  Caesar   Vigenère  Stream   S-DES        │
                       │        │           │
                       │        │           │
                       └────────┴───────────┘
                                │
                                ▼
                        4 Tahap Berurutan
                                │
                         Caesar → Vigenère
                                ↓
                        XOR + LFSR → S-DES
                                │
                                ▼
                         Ciphertext HEX
```

---

# 11. Contoh Alur Super Enkripsi

Misalkan pengguna memasukkan:

```text
Plaintext:
Kriptografi Modern
```

dengan:

```text
Kunci Caesar  : 3
Kunci Vigenère: KUNCI
Seed LFSR     : 1111
Kunci S-DES   : 1010000010
```

Maka alurnya:

```text
"Kriptografi Modern"
          │
          ▼
    Caesar Cipher
          │
          ▼
     Hasil Caesar
          │
          ▼
   Vigenère Cipher
          │
          ▼
    Hasil Vigenère
          │
          ▼
    Text → Byte
          │
          ▼
      LFSR
          │
          ▼
      Keystream
          │
          ▼
         XOR
          │
          ▼
   Hasil Stream Cipher
          │
          ▼
        S-DES
          │
          ▼
    Ciphertext HEX
```

Aplikasi kemudian menampilkan hasil setiap tahap beserta tabel prosesnya.

---

# 12. Catatan Penting

Aplikasi ini dibuat terutama sebagai **media pembelajaran dan demonstrasi algoritma kriptografi**.

Algoritma yang digunakan memiliki karakteristik yang berbeda:

| Algoritma      | Jenis                  | Fungsi                       |
| -------------- | ---------------------- | ---------------------------- |
| Caesar         | Kriptografi klasik     | Substitusi sederhana         |
| Vigenère       | Kriptografi klasik     | Substitusi polialfabetik     |
| XOR + LFSR     | Stream cipher edukatif | Pembangkitan keystream + XOR |
| S-DES          | Block cipher edukatif  | Enkripsi blok 8-bit          |
| Super Enkripsi | Kombinasi              | Menggabungkan 4 tahap        |

**Catatan keamanan:** implementasi XOR + LFSR pada aplikasi ini ditujukan untuk pembelajaran konsep stream cipher. LFSR sederhana bukan pengganti algoritma kriptografi modern yang telah dirancang dan diuji untuk penggunaan keamanan nyata.

Selain itu, implementasi LFSR pada kode saat ini menghitung feedback tetapi belum memperbarui register pada setiap iterasi. Jika digunakan sebagai implementasi LFSR yang lebih tepat, register perlu di-*shift* setelah feedback dihitung.

---

# 13. Tujuan Pembelajaran

Melalui aplikasi ini, pengguna dapat memahami:

* konsep plaintext dan ciphertext,
* penggunaan key dalam proses enkripsi/dekripsi,
* prinsip substitusi pada Caesar,
* konsep polyalphabetic substitution pada Vigenère,
* konsep keystream pada stream cipher,
* penggunaan LFSR sebagai generator keystream,
* operasi XOR,
* konsep block cipher melalui S-DES,
* proses pembentukan sub-key S-DES,
* konsep kombinasi beberapa algoritma melalui super enkripsi,
* serta hubungan antara proses enkripsi dan dekripsi.

---

# 14. Ringkasan Arsitektur

```text
INPUT
  │
  ├── Caesar
  │
  ├── Vigenère
  │
  ├── Stream Cipher
  │      ├── Seed
  │      ├── LFSR
  │      ├── Keystream
  │      └── XOR
  │
  └── S-DES
         ├── Key 10-bit
         ├── K1
         ├── K2
         ├── Permutation
         ├── S-Box
         └── XOR

             ↓

      CIPHERTEXT (HEX)
```

## 👨‍💻 Catatan

Aplikasi ini dibuat untuk keperluan pembelajaran mata kuliah **Kriptografi**, dengan fokus pada pemahaman proses algoritma melalui implementasi dan visualisasi langkah-langkah enkripsi serta dekripsi.


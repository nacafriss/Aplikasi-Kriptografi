import streamlit as st

from menu1_caesar_chipher import tampilkan_halaman_caesar
from menu2_vigenere import tampilkan_halaman_vigenere
from menu3_stream_cipher import tampilkan_halaman_stream_cipher
from menu4_block_cipher import tampilkan_halaman_block_cipher
from menu5_super_enkripsi import tampilkan_halaman_super


st.set_page_config(page_title="Aplikasi Kriptografi", layout="wide")

st.sidebar.title("Aplikasi Kriptografi")

daftar_menu = [
    "Caesar Cipher (Klasik)",
    "Vigenère Cipher (Klasik)",
    "Stream Cipher — XOR & LFSR (Modern)",
    "Block Cipher — S-DES (Modern)",
    "Super Enkripsi (Gabungan)",
]

menu_dipilih = st.sidebar.radio("Pilih Menu", daftar_menu)

if menu_dipilih == "Caesar Cipher (Klasik)":
    tampilkan_halaman_caesar()

elif menu_dipilih == "Vigenère Cipher (Klasik)":
    tampilkan_halaman_vigenere()

elif menu_dipilih == "Stream Cipher — XOR & LFSR (Modern)":
    tampilkan_halaman_stream_cipher()

elif menu_dipilih == "Block Cipher — S-DES (Modern)":
    tampilkan_halaman_block_cipher()

elif menu_dipilih == "Super Enkripsi (Gabungan)":
    tampilkan_halaman_super()




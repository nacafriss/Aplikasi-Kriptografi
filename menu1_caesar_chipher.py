import streamlit as st
import pandas as pd

from utils import tampilkan_karakter

def caesar_process(teks, kunci_geser, mode):

    if mode == "Enkripsi":
        arah_geser = kunci_geser
    else:
        arah_geser = -kunci_geser

    huruf_hasil = []
    langkah = []

    for nomor, karakter in enumerate(teks, start=1):
        if karakter.isalpha():
            if karakter.isupper():
                huruf_dasar = 65
            else:
                huruf_dasar = 97

            posisi_awal = ord(karakter) - huruf_dasar

            posisi_baru = (posisi_awal + arah_geser) % 26

            huruf_baru = chr(posisi_baru + huruf_dasar)

            tanda_operasi = '+' if mode == "Enkripsi" else '-'
            langkah.append({
                "No": nomor,
                "Karakter": tampilkan_karakter(karakter),
                "Posisi (0-25)": posisi_awal,
                "Pergeseran": arah_geser,
                "Rumus": f"({posisi_awal} {tanda_operasi} {kunci_geser}) mod 26 = {posisi_baru}",
                "Hasil": tampilkan_karakter(huruf_baru),
            })
            huruf_hasil.append(huruf_baru)
        else:
            langkah.append({
                "No": nomor,
                "Karakter": tampilkan_karakter(karakter),
                "Posisi (0-25)": "-",
                "Pergeseran": "-",
                "Rumus": "bukan huruf, tidak diubah",
                "Hasil": tampilkan_karakter(karakter),
            })
            huruf_hasil.append(karakter)

    hasil_teks = ''.join(huruf_hasil)
    return hasil_teks, langkah


def tampilkan_halaman_caesar():

    st.title("Caesar Cipher (Klasik)")
    st.caption("Algoritma substitusi klasik: setiap huruf digeser sejauh *n* posisi dalam alfabet.")

    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], horizontal=True)

    label_teks = "Plainteks" if mode == "Enkripsi" else "Cipherteks"
    teks = st.text_area(f"Teks {label_teks}", "Kriptografi Modern")

    kunci_geser = st.number_input("Kunci (nilai pergeseran)", min_value=1, max_value=25, value=3)

    if st.button("Proses", key="btn_caesar"):
        hasil, langkah = caesar_process(teks, kunci_geser, mode)
        st.success(f"Hasil {mode}: **{hasil}**")

        with st.expander("Lihat Proses Algoritma (langkah demi langkah)", expanded=True):
            st.dataframe(pd.DataFrame(langkah), use_container_width=True, hide_index=True)

import streamlit as st
import pandas as pd

from utils import tampilkan_karakter

def vigenere_process(teks, kata_kunci, mode):

    huruf_kunci = ''.join(huruf for huruf in kata_kunci if huruf.isalpha())
    if huruf_kunci == "":
        huruf_kunci = "KUNCI"

    huruf_hasil = []
    langkah = []
    indeks_kunci = 0 

    for nomor, karakter in enumerate(teks, start=1):
        if karakter.isalpha():
            huruf_kunci_aktif = huruf_kunci[indeks_kunci % len(huruf_kunci)].upper()
            nilai_geser_kunci = ord(huruf_kunci_aktif) - 65

            if karakter.isupper():
                huruf_dasar = 65
            else:
                huruf_dasar = 97

            posisi_awal = ord(karakter) - huruf_dasar

            if mode == "Enkripsi":
                posisi_baru = (posisi_awal + nilai_geser_kunci) % 26
                rumus = f"({posisi_awal} + {nilai_geser_kunci}) mod 26 = {posisi_baru}"
            else:
                posisi_baru = (posisi_awal - nilai_geser_kunci) % 26
                rumus = f"({posisi_awal} - {nilai_geser_kunci}) mod 26 = {posisi_baru}"

            huruf_baru = chr(posisi_baru + huruf_dasar)

            langkah.append({
                "No": nomor,
                "Karakter": tampilkan_karakter(karakter),
                "Huruf Kunci": huruf_kunci_aktif,
                "Nilai Kunci": nilai_geser_kunci,
                "Rumus": rumus,
                "Hasil": tampilkan_karakter(huruf_baru),
            })
            huruf_hasil.append(huruf_baru)

            indeks_kunci += 1
        else:
            langkah.append({
                "No": nomor,
                "Karakter": tampilkan_karakter(karakter),
                "Huruf Kunci": "-",
                "Nilai Kunci": "-",
                "Rumus": "bukan huruf, tidak diubah",
                "Hasil": tampilkan_karakter(karakter),
            })
            huruf_hasil.append(karakter)

    hasil_teks = ''.join(huruf_hasil)
    return hasil_teks, langkah


def tampilkan_halaman_vigenere():

    st.title("Vigenère Cipher (Klasik)")
    st.caption(
        "Algoritma substitusi polialfabetik: pergeseran tiap huruf "
        "ditentukan oleh huruf kata kunci yang berulang."
    )

    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], horizontal=True, key="mode_vig")

    label_teks = "Plainteks" if mode == "Enkripsi" else "Cipherteks"
    teks = st.text_area(f"Teks {label_teks}", "Kriptografi Modern", key="text_vig")

    kata_kunci = st.text_input("Kata Kunci", "KUNCI")

    if st.button("Proses", key="btn_vig"):
        hasil, langkah = vigenere_process(teks, kata_kunci, mode)
        st.success(f"Hasil {mode}: **{hasil}**")

        with st.expander("Lihat Proses Algoritma (langkah demi langkah)", expanded=True):
            st.dataframe(pd.DataFrame(langkah), use_container_width=True, hide_index=True)

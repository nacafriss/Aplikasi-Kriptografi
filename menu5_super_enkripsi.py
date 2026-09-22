import streamlit as st
import pandas as pd

from utils import text_to_bytes, bytes_to_text, bytes_to_hex, hex_to_bytes
from menu1_caesar_chipher import caesar_process
from menu2_vigenere import vigenere_process
from menu3_stream_cipher import xor_stream_process
from menu4_block_cipher import sdes_key_process


def super_encrypt(plainteks, kunci_caesar, kunci_vigenere, seed_lfsr, kunci_sdes):

    tahap1, langkah1 = caesar_process(plainteks, kunci_caesar, "Enkripsi")

    tahap2, langkah2 = vigenere_process(tahap1, kunci_vigenere, "Enkripsi")

    byte_tahap2 = text_to_bytes(tahap2)
    byte_tahap3, langkah3, jejak_lfsr = xor_stream_process(byte_tahap2, seed_lfsr, "Enkripsi")

    byte_tahap4, langkah4, k1, k2 = sdes_key_process(byte_tahap3, kunci_sdes, "Enkripsi")

    hex_akhir = bytes_to_hex(byte_tahap4)

    catatan_proses = {
        "stage1_caesar": tahap1, "s1_steps": langkah1,
        "stage2_vigenere": tahap2, "s2_steps": langkah2,
        "stage3_xor_hex": bytes_to_hex(byte_tahap3), "s3_steps": langkah3, "lfsr_trace": jejak_lfsr,
        "stage4_sdes_hex": hex_akhir, "s4_steps": langkah4, "k1": k1, "k2": k2,
    }
    return hex_akhir, catatan_proses


def super_decrypt(cipher_hex, kunci_caesar, kunci_vigenere, seed_lfsr, kunci_sdes):

    byte_tahap4 = hex_to_bytes(cipher_hex)
    byte_tahap3, langkah4, k1, k2 = sdes_key_process(byte_tahap4, kunci_sdes, "Dekripsi")

    byte_tahap2, langkah3, jejak_lfsr = xor_stream_process(byte_tahap3, seed_lfsr, "Dekripsi")
    tahap2 = bytes_to_text(byte_tahap2)

    tahap1, langkah2 = vigenere_process(tahap2, kunci_vigenere, "Dekripsi")

    plainteks_asli, langkah1 = caesar_process(tahap1, kunci_caesar, "Dekripsi")

    catatan_proses = {
        "stage4_sdes_hex": bytes_to_hex(byte_tahap4), "s4_steps": langkah4, "k1": k1, "k2": k2,
        "stage3_xor_hex": bytes_to_hex(byte_tahap3), "s3_steps": langkah3, "lfsr_trace": jejak_lfsr,
        "stage2_vigenere": tahap2, "s2_steps": langkah2,
        "stage1_caesar": tahap1, "s1_steps": langkah1,
    }
    return plainteks_asli, catatan_proses


def tampilkan_halaman_super():
    """Menampilkan seluruh tampilan (UI) untuk menu Super Enkripsi."""

    st.title("Super Enkripsi")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], horizontal=True, key="mode_super")

    kolom1, kolom2 = st.columns(2)
    with kolom1:
        kunci_caesar = st.number_input("Kunci Caesar (pergeseran)", min_value=1, max_value=25, value=3)
        kunci_vigenere = st.text_input("Kunci Vigenère", "KUNCI")
    with kolom2:
        seed_lfsr = st.text_input("Seed LFSR (biner)", "1111")
        kunci_sdes = st.text_input("Kunci S-DES (10-bit biner)", "1010000010")

    seed_valid = bool(seed_lfsr) and set(seed_lfsr) <= {"0", "1"} and any(bit == "1" for bit in seed_lfsr)
    kunci_sdes_valid = len(kunci_sdes) == 10 and set(kunci_sdes) <= {"0", "1"}

    if not seed_valid:
        st.error("Seed LFSR harus biner, tidak boleh semua nol.")
        return
    if not kunci_sdes_valid:
        st.error("Kunci S-DES harus 10 digit biner.")
        return

    if mode == "Enkripsi":
        teks = st.text_area("Plainteks", "Kriptografi Modern")
        if st.button("Enkripsi (Super)", key="btn_super_enc"):
            hex_akhir, catatan = super_encrypt(teks, kunci_caesar, kunci_vigenere, seed_lfsr, kunci_sdes)
            st.success(f"Cipherteks Akhir (HEX): **{hex_akhir}**")

            st.subheader("Halaman Proses — 4 Tahap Enkripsi")
            with st.expander("Tahap 1 — Caesar Cipher", expanded=False):
                st.write(f"Hasil setelah Caesar: `{catatan['stage1_caesar']}`")
                st.dataframe(pd.DataFrame(catatan["s1_steps"]), use_container_width=True, hide_index=True)
            with st.expander("Tahap 2 — Vigenère Cipher", expanded=False):
                st.write(f"Hasil setelah Vigenère: `{catatan['stage2_vigenere']}`")
                st.dataframe(pd.DataFrame(catatan["s2_steps"]), use_container_width=True, hide_index=True)
            with st.expander("Tahap 3 — Stream Cipher (XOR/LFSR)", expanded=False):
                st.write(f"Hasil setelah XOR (HEX): `{catatan['stage3_xor_hex']}`")
                st.write("Jejak pembangkitan keystream LFSR:")
                st.dataframe(pd.DataFrame(catatan["lfsr_trace"]), use_container_width=True, hide_index=True)
                st.dataframe(pd.DataFrame(catatan["s3_steps"]), use_container_width=True, hide_index=True)
            with st.expander("Tahap 4 — Block Cipher (S-DES)", expanded=True):
                st.write(f"Sub-kunci → K1 = `{catatan['k1']}` | K2 = `{catatan['k2']}`")
                st.write(f"Hasil akhir (HEX): `{catatan['stage4_sdes_hex']}`")
                st.dataframe(pd.DataFrame(catatan["s4_steps"]), use_container_width=True, hide_index=True)
    else:
        cipher_hex = st.text_area("Cipherteks (HEX)", "")
        if st.button("Dekripsi (Super)", key="btn_super_dec"):
            try:
                plainteks, catatan = super_decrypt(cipher_hex, kunci_caesar, kunci_vigenere, seed_lfsr, kunci_sdes)
                st.success(f"Plainteks Akhir: **{plainteks}**")

                st.subheader("Halaman Proses — 4 Tahap Dekripsi")
                with st.expander("Tahap 1 — Block Cipher (S-DES) Dekripsi", expanded=False):
                    st.write(f"Sub-kunci → K1 = `{catatan['k1']}` | K2 = `{catatan['k2']}`")
                    st.write(f"Hasil setelah dekripsi S-DES (HEX): `{catatan['stage4_sdes_hex']}`")
                    st.dataframe(pd.DataFrame(catatan["s4_steps"]), use_container_width=True, hide_index=True)
                with st.expander("Tahap 2 — Stream Cipher (XOR/LFSR) Dekripsi", expanded=False):
                    st.write(f"Hasil setelah XOR (HEX): `{catatan['stage3_xor_hex']}`")
                    st.dataframe(pd.DataFrame(catatan["lfsr_trace"]), use_container_width=True, hide_index=True)
                    st.dataframe(pd.DataFrame(catatan["s3_steps"]), use_container_width=True, hide_index=True)
                with st.expander("Tahap 3 — Vigenère Cipher Dekripsi", expanded=False):
                    st.write(f"Hasil setelah Vigenère: `{catatan['stage2_vigenere']}`")
                    st.dataframe(pd.DataFrame(catatan["s2_steps"]), use_container_width=True, hide_index=True)
                with st.expander("Tahap 4 — Caesar Cipher Dekripsi", expanded=True):
                    st.write(f"Hasil akhir (plainteks): `{catatan['stage1_caesar']}`")
                    st.dataframe(pd.DataFrame(catatan["s1_steps"]), use_container_width=True, hide_index=True)
            except ValueError as error:
                st.error(f"Format HEX tidak valid: {error}")

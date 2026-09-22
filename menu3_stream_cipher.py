import streamlit as st
import pandas as pd

from utils import text_to_bytes, bytes_to_text, bytes_to_hex, hex_to_bytes, byte_to_bits

def lfsr_keystream(seed_bit: str, panjang: int):
    register = [int(bit) for bit in seed_bit]

    bit_keluaran = []
    jejak_proses = []

    for langkah_ke in range(panjang):
        bit_keluar = register[-1]  
        bit_feedback = register[0] ^ register[-1]  

        jejak_proses.append({
            "Clock ke-": langkah_ke + 1,
            "Register (b1..bn)": ''.join(str(bit) for bit in register),
            "Keluaran (bn)": bit_keluar,
            "Feedback (b1 XOR bn)": bit_feedback,
        })

        bit_keluaran.append(bit_keluar)

    return bit_keluaran, jejak_proses


def xor_stream_process(daftar_byte, seed_bit, mode):

    total_bit_dibutuhkan = len(daftar_byte) * 8
    bit_keystream, jejak_lfsr = lfsr_keystream(seed_bit, total_bit_dibutuhkan)

    hasil_byte = []
    langkah = []

    for nomor, byte_asal in enumerate(daftar_byte):
        bit_plainteks = byte_to_bits(byte_asal)

        potongan_keystream = bit_keystream[nomor * 8: (nomor + 1) * 8]
        bit_keystream_teks = ''.join(str(bit) for bit in potongan_keystream)
        bit_hasil = ''.join(
            str(int(p) ^ int(k)) for p, k in zip(bit_plainteks, bit_keystream_teks)
        )
        byte_hasil = int(bit_hasil, 2)

        hasil_byte.append(byte_hasil)
        langkah.append({
            "No": nomor + 1,
            "Byte Masukan": f"{byte_asal:3d}",
            "Bit Masukan": bit_plainteks,
            "Bit Keystream": bit_keystream_teks,
            "XOR": f"{bit_plainteks} XOR {bit_keystream_teks}",
            "Bit Hasil": bit_hasil,
            "Byte Hasil": byte_hasil,
        })

    return hasil_byte, langkah, jejak_lfsr


def tampilkan_halaman_stream_cipher():

    st.title("Stream Cipher (Operasi XOR + LFSR Keystream Generator)")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], horizontal=True, key="mode_xor")
    seed = st.text_input("Seed / Kunci LFSR (biner, tidak boleh semua 0)", "1111")

    seed_valid = bool(seed) and set(seed) <= {"0", "1"} and any(bit == "1" for bit in seed)

    if not seed_valid:
        st.error("Seed harus berupa string biner (hanya 0/1) dan tidak boleh semua nol.")
        return

    if mode == "Enkripsi":
        teks = st.text_area("Plainteks", "Kriptografi Modern")
        if st.button("Enkripsi", key="btn_xor_enc"):
            daftar_byte = text_to_bytes(teks)
            hasil_byte, langkah, jejak_lfsr = xor_stream_process(daftar_byte, seed, mode)

            st.success(f"Cipherteks (HEX): **{bytes_to_hex(hasil_byte)}**")

            with st.expander("Proses Pembangkitan Keystream (LFSR)", expanded=False):
                st.dataframe(pd.DataFrame(jejak_lfsr), use_container_width=True, hide_index=True)
            with st.expander("Proses Operasi XOR per Byte", expanded=True):
                st.dataframe(pd.DataFrame(langkah), use_container_width=True, hide_index=True)
    else:
        cipher_hex = st.text_area("Cipherteks (HEX)", "")
        if st.button("Dekripsi", key="btn_xor_dec"):
            try:
                daftar_byte = hex_to_bytes(cipher_hex)
                hasil_byte, langkah, jejak_lfsr = xor_stream_process(daftar_byte, seed, mode)

                st.success(f"Plainteks: **{bytes_to_text(hasil_byte)}**")

                with st.expander("Proses Pembangkitan Keystream (LFSR)", expanded=False):
                    st.dataframe(pd.DataFrame(jejak_lfsr), use_container_width=True, hide_index=True)
                with st.expander("Proses Operasi XOR per Byte", expanded=True):
                    st.dataframe(pd.DataFrame(langkah), use_container_width=True, hide_index=True)
            except ValueError as error:
                st.error(f"Format HEX tidak valid: {error}")

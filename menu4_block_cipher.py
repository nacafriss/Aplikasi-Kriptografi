import streamlit as st
import pandas as pd

from utils import text_to_bytes, bytes_to_text, bytes_to_hex, hex_to_bytes, byte_to_bits

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]      
P8 = [6, 3, 7, 4, 8, 5, 10, 9]              
IP = [2, 6, 3, 1, 4, 8, 5, 7]               
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]           
EP = [4, 1, 2, 3, 2, 3, 4, 1]                
P4 = [2, 4, 3, 1]                            

S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]


def permute(bit_teks, tabel_urutan):
    return ''.join(bit_teks[posisi - 1] for posisi in tabel_urutan)


def left_shift(bit_teks, jumlah_geser):
    return bit_teks[jumlah_geser:] + bit_teks[:jumlah_geser]


def xor_bits(bit_a, bit_b):
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(bit_a, bit_b))

def sbox_lookup(empat_bit, sbox):

    baris = int(empat_bit[0] + empat_bit[3], 2)
    kolom = int(empat_bit[1] + empat_bit[2], 2)
    nilai = sbox[baris][kolom]
    return format(nilai, '02b')


def sdes_generate_keys(kunci_10bit: str):
    hasil_p10 = permute(kunci_10bit, P10)
    bagian_kiri, bagian_kanan = hasil_p10[:5], hasil_p10[5:]

    kiri_1, kanan_1 = left_shift(bagian_kiri, 1), left_shift(bagian_kanan, 1)
    k1 = permute(kiri_1 + kanan_1, P8)

    kiri_2, kanan_2 = left_shift(kiri_1, 2), left_shift(kanan_1, 2)
    k2 = permute(kiri_2 + kanan_2, P8)

    return k1, k2

def sdes_fk(delapan_bit, sub_kunci):
    kiri, kanan = delapan_bit[:4], delapan_bit[4:]

    hasil_ep = permute(kanan, EP)          
    hasil_xor = xor_bits(hasil_ep, sub_kunci)

    setengah_kiri, setengah_kanan = hasil_xor[:4], hasil_xor[4:]
    keluaran_s0 = sbox_lookup(setengah_kiri, S0)
    keluaran_s1 = sbox_lookup(setengah_kanan, S1)

    hasil_p4 = permute(keluaran_s0 + keluaran_s1, P4)
    kiri_baru = xor_bits(kiri, hasil_p4)

    return kiri_baru + kanan


def sdes_process_block(delapan_bit, k1, k2, mode):
    if mode == "Enkripsi":
        kunci_pertama, kunci_kedua = k1, k2
    else:
        kunci_pertama, kunci_kedua = k2, k1

    hasil_ip = permute(delapan_bit, IP)
    hasil_fk1 = sdes_fk(hasil_ip, kunci_pertama)

    hasil_swap = hasil_fk1[4:] + hasil_fk1[:4]

    hasil_fk2 = sdes_fk(hasil_swap, kunci_kedua)
    hasil_akhir = permute(hasil_fk2, IP_INV)

    rincian_proses = {
        "IP": hasil_ip,
        "Setelah fK1": hasil_fk1,
        "Setelah Swap": hasil_swap,
        "Setelah fK2": hasil_fk2,
        "IP-1 (hasil)": hasil_akhir,
    }
    return hasil_akhir, rincian_proses

def teks_ke_kunci_10bit(kunci_teks: str):
    """Konversi kunci berupa plain text menjadi kunci 10-bit biner.

    Setiap karakter diubah ke kode ASCII, lalu ke 8-bit biner, seluruh bit
    digabung, kemudian diambil/dipotong menjadi 10 bit (jika kurang dari
    10 bit maka akan di-pad dengan '0' di sebelah kanan).
    """
    daftar_byte = text_to_bytes(kunci_teks)

    rincian = []
    semua_bit = ""
    for nomor, (karakter, byte_asal) in enumerate(zip(kunci_teks, daftar_byte)):
        bit8 = byte_to_bits(byte_asal)
        semua_bit += bit8
        rincian.append({
            "No": nomor + 1,
            "Karakter": karakter,
            "Kode ASCII": byte_asal,
            "8-bit Biner": bit8,
        })

    if len(semua_bit) >= 10:
        kunci_10bit = semua_bit[:10]
        keterangan = f"Diambil 10 bit pertama dari {len(semua_bit)} bit hasil gabungan."
    else:
        kunci_10bit = semua_bit.ljust(10, "0")
        keterangan = f"Bit hasil gabungan hanya {len(semua_bit)} bit, di-pad '0' di kanan hingga 10 bit."

    return kunci_10bit, semua_bit, rincian, keterangan


def sdes_key_process(daftar_byte, kunci_10bit, mode):
    k1, k2 = sdes_generate_keys(kunci_10bit)

    hasil_byte = []
    langkah = []

    for nomor, byte_asal in enumerate(daftar_byte):
        delapan_bit = byte_to_bits(byte_asal)
        bit_hasil, rincian = sdes_process_block(delapan_bit, k1, k2, mode)
        byte_hasil = int(bit_hasil, 2)

        hasil_byte.append(byte_hasil)
        langkah.append({
            "No": nomor + 1,
            "Byte Masukan": byte_asal,
            "Bit Masukan": delapan_bit,
            "IP": rincian["IP"],
            "Setelah fK1": rincian["Setelah fK1"],
            "Swap": rincian["Setelah Swap"],
            "Setelah fK2": rincian["Setelah fK2"],
            "Bit Hasil": rincian["IP-1 (hasil)"],
            "Byte Hasil": byte_hasil,
            "Byte Hasil (HEX)": f"{byte_hasil:02X}",
        })

    return hasil_byte, langkah, k1, k2


def tampilkan_halaman_block_cipher():
    st.title("Block Cipher (S-DES / Simplified DES)")

    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"], horizontal=True, key="mode_sdes")
    kunci_teks = st.text_input("Kunci (plain text)", "KU")

    if not kunci_teks:
        st.error("Kunci tidak boleh kosong.")
        return

    kunci_10bit, semua_bit, rincian_kunci, keterangan_kunci = teks_ke_kunci_10bit(kunci_teks)

    with st.expander("Proses Konversi Kunci: Plain Text → 10-bit Biner", expanded=True):
        st.dataframe(pd.DataFrame(rincian_kunci), use_container_width=True, hide_index=True)
        st.write(f"Gabungan seluruh bit: `{semua_bit}`")
        st.write(keterangan_kunci)
        st.success(f"Kunci 10-bit yang digunakan: **{kunci_10bit}**")

    if mode == "Enkripsi":
        teks = st.text_area("Plainteks", "Modern")
        if st.button("Enkripsi", key="btn_sdes_enc"):
            daftar_byte = text_to_bytes(teks)
            hasil_byte, langkah, k1, k2 = sdes_key_process(daftar_byte, kunci_10bit, mode)

            st.info(f"Sub-kunci internal → K1 = `{k1}`  |  K2 = `{k2}`")
            st.success(f"Cipherteks (HEX): **{bytes_to_hex(hasil_byte)}**")

            with st.expander("Proses S-DES per Blok (8-bit)", expanded=True):
                st.dataframe(pd.DataFrame(langkah), use_container_width=True, hide_index=True)
    else:
        cipher_hex = st.text_area("Cipherteks (HEX)", "")
        if st.button("Dekripsi", key="btn_sdes_dec"):
            try:
                daftar_byte = hex_to_bytes(cipher_hex)
                hasil_byte, langkah, k1, k2 = sdes_key_process(daftar_byte, kunci_10bit, mode)

                st.info(f"Sub-kunci internal → K1 = `{k1}`  |  K2 = `{k2}`")
                st.success(f"Plainteks: **{bytes_to_text(hasil_byte)}**")

                with st.expander("Proses S-DES per Blok (8-bit)", expanded=True):
                    st.dataframe(pd.DataFrame(langkah), use_container_width=True, hide_index=True)
            except ValueError as error:
                st.error(f"Format HEX tidak valid: {error}")
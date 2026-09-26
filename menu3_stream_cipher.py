import streamlit as st
import pandas as pd

from utils import text_to_bytes, bytes_to_text, bytes_to_base64, base64_to_bytes, base64_to_bytes_process, byte_to_bits

def lfsr_keystream(seed_bit, panjang):
    register = [int(bit) for bit in seed_bit]
    keystream = []
    jejak_proses = []

    for langkah in range(panjang):
        # Ambil output dari bit terakhir register
        bit_keluar = register[-1]

        # Hitung feedback
        bit_feedback = register[0] ^ register[-1]

        # Simpan bit ke keystream
        keystream.append(bit_keluar)

        # 4. Mencatat proses
        jejak_proses.append({
            "Clock": langkah + 1,
            "Register": ''.join(map(str, register)),
            "Output": bit_keluar,
            "Feedback": bit_feedback
        })

        # Shift register
        register = [bit_feedback] + register[:-1]

    return keystream, jejak_proses


def xor_stream_process(daftar_byte, seed_bit, mode):

    # jumlah bit yang dibutuhkan
    total_bit_dibutuhkan = len(daftar_byte) * 8
    
    # membangkitkan keystream pake LFSR
    bit_keystream, jejak_lfsr = lfsr_keystream(
        seed_bit, 
        total_bit_dibutuhkan)

    hasil_byte = []
    langkah = []

    for nomor, byte_asal in enumerate(daftar_byte):

        # mengubah byte menjadi 8 bit
        bit_plainteks = byte_to_bits(byte_asal)

        potongan_keystream = bit_keystream[nomor * 8: (nomor + 1) * 8]
        
        bit_keystream_teks = ''.join(
            str(bit) for bit in potongan_keystream)
        

        # XOR setiap bit
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

    st.title("Stream Cipher ")
    st.caption("Operasi XOR + LFSR Keystream Generator")

    mode = st.radio("Mode", 
                    ["Enkripsi", "Dekripsi"], 
                    horizontal=True, 
                    key="mode_xor")
    seed = st.text_input("Seed / Kunci LFSR (biner, tidak boleh semua 0)", "1111")

    seed_valid = bool(seed) and set(seed) <= {"0", "1"} and any(bit == "1" for bit in seed)

    if not seed_valid:
        st.error("Seed harus berupa string biner (hanya 0/1) dan tidak boleh semua nol.")
        return


    if mode == "Enkripsi":
        teks = st.text_area("Plainteks", "Kriptografi Modern")
        if st.button("Enkripsi", 
                     key="btn_xor_enc"):
            daftar_byte = text_to_bytes(teks)
            daftar_bit = [
                byte_to_bits(byte)
                for byte in daftar_byte
            ]
            hasil_byte, langkah, jejak_lfsr = xor_stream_process(
                daftar_byte, 
                seed, 
                mode
            )

            cipherteks = bytes_to_base64(hasil_byte)

            st.success(f"Cipherteks: **{cipherteks}**")

            with st.expander(
                "Plaintext → Byte",
                expanded=False
            ):

                st.write(
                    "Plaintext diubah terlebih dahulu menjadi byte."
                )

                data_byte = []

                for karakter, byte in zip(
                    teks,
                    daftar_byte
                ):
                    data_byte.append({
                        "Karakter": karakter,
                        "Byte": byte
                    })

                st.dataframe(
                    pd.DataFrame(data_byte),
                    use_container_width=True,
                    hide_index=True
                )

            with st.expander(
                "Byte → Bit",
                expanded=False
            ):

                st.write(
                    "Setiap byte direpresentasikan sebagai 8 bit "
                    "karena operasi XOR dilakukan pada level bit."
                )

                data_bit = []

                for nomor, (byte, bit) in enumerate(
                    zip(daftar_byte, daftar_bit),
                    start=1
                ):
                    data_bit.append({
                        "No": nomor,
                        "Byte": byte,
                        "Bit": bit
                    })

                st.dataframe(
                    pd.DataFrame(data_bit),
                    use_container_width=True,
                    hide_index=True
                )

            with st.expander(
                "Pembangkitan Keystream dengan LFSR",
                expanded=False
            ):

                st.write(
                    f"Seed LFSR: **{seed}**"
                )

                st.write(
                    "LFSR digunakan untuk menghasilkan "
                    "keystream yang akan digunakan pada operasi XOR."
                )

                st.dataframe(
                    pd.DataFrame(jejak_lfsr),
                    use_container_width=True,
                    hide_index=True
                )

                st.write(
                    f"Total bit keystream yang dihasilkan: "
                    f"**{len(jejak_lfsr)} bit**"
                )

            with st.expander(
                "Operasi XOR",
                expanded=False
            ):

                st.write(
                    "Setiap bit plaintext di-XOR dengan "
                    "bit keystream."
                )

                st.dataframe(
                    pd.DataFrame(langkah),
                    use_container_width=True,
                    hide_index=True
                )

            with st.expander(
                "Ciphertext Byte → Base64",
                expanded=True
            ):

                st.write(
                    "Hasil XOR berupa byte. Byte tersebut "
                    "kemudian di-encode menggunakan Base64 "
                    "agar ciphertext dapat ditampilkan sebagai "
                    "teks."
                )

                data_cipher = []

                for nomor, byte in enumerate(
                    hasil_byte,
                    start=1
                ):
                    data_cipher.append({
                        "No": nomor,
                        "Ciphertext Byte": byte,
                        "Base64": bytes([byte])
                    })

                st.write(
                    f"Ciphertext Base64: **{cipherteks}**"
                )
    else:
        cipher_base64 = st.text_area(
            "Cipherteks (Base64)",
        )

        if st.button(
            "Dekripsi",
            key="btn_xor_dec"
        ):

            try:            
                daftar_byte, proses_base64 = base64_to_bytes_process(
                    cipher_base64.strip()
                )           

                hasil_byte, langkah, jejak_lfsr = xor_stream_process(
                    daftar_byte,
                    seed,
                    mode
                )

                plaintext = bytes_to_text(
                    hasil_byte
                )

                st.success(
                    f"Plainteks: **{plaintext}**"
                )

                with st.expander(
                    "Ciphertext Base64 → Byte",
                    expanded=False
                ):

                    st.write(
                        "Ciphertext Base64 dikembalikan terlebih dahulu "
                        "menjadi byte ciphertext."
                    )
                    st.dataframe(
                        pd.DataFrame(proses_base64),
                        use_container_width=True,
                        hide_index=True
                    )

                    st.write(
                        f"**Ciphertext Byte:** `{daftar_byte}`"
                    )

                with st.expander(
                    "Pembangkitan Keystream dengan LFSR",
                    expanded=False
                ):

                    st.write(
                        f"Seed LFSR: **{seed}**"
                    )

                    st.write(
                        "Dekripsi menggunakan seed yang sama "
                        "untuk menghasilkan keystream yang sama."
                    )

                    st.dataframe(
                        pd.DataFrame(jejak_lfsr),
                        use_container_width=True,
                        hide_index=True
                    )

                with st.expander(
                    "Operasi XOR",
                    expanded=False
                ):

                    st.write(
                        "Ciphertext di-XOR kembali dengan "
                        "keystream untuk mendapatkan plaintext."
                    )

                    st.dataframe(
                        pd.DataFrame(langkah),
                        use_container_width=True,
                        hide_index=True
                    )

                with st.expander(
                    "Byte → Plaintext",
                    expanded=False
                ):

                    st.write(
                        "Hasil XOR berupa byte kemudian "
                        "dikonversi kembali menjadi teks UTF-8."
                    )

                    data_plaintext = []

                    for karakter, byte in zip(
                        plaintext,
                        hasil_byte
                    ):
                        data_plaintext.append({
                            "Karakter": karakter,
                            "Byte": byte,
                            "Bit": byte_to_bits(byte)
                        })

                    st.dataframe(
                        pd.DataFrame(data_plaintext),
                        use_container_width=True,
                        hide_index=True
                    )

            except Exception as error:

                st.error(
                    f"Cipherteks Base64 tidak valid: {error}"
                )

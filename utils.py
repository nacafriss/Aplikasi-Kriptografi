import base64

def text_to_bytes(teks: str):
    daftar_byte = []
    for huruf in teks:
        daftar_byte.append(ord(huruf))
    return daftar_byte


def bytes_to_text(daftar_byte):
    huruf_huruf = []
    for byte in daftar_byte:
        huruf_huruf.append(chr(byte))
    return ''.join(huruf_huruf)


def bytes_to_hex(daftar_byte):
    return ''.join(f'{byte:02X}' for byte in daftar_byte)


def hex_to_bytes(teks_hex: str):
    teks_hex = teks_hex.strip().replace(' ', '').replace('\n', '')

    if len(teks_hex) % 2 != 0:
        raise ValueError("Panjang string HEX harus genap.")

    hasil = []
    for i in range(0, len(teks_hex), 2):
        dua_digit = teks_hex[i:i + 2]
        hasil.append(int(dua_digit, 16))
    return hasil


def byte_to_bits(byte, jumlah_bit=8):
    return format(byte, f'0{jumlah_bit}b')

def bytes_to_base64(data):
    return base64.b64encode(bytes(data)).decode("utf-8")

def base64_to_bytes(teks):
    return list(base64.b64decode(teks, validate=True))

def base64_to_bytes_process(teks):
    tabel_base64 = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789+/"
    )

    proses = []

    # Hilangkan padding '=' untuk proses karakter
    teks_tanpa_padding = teks.rstrip("=")

    semua_bit = ""

    for karakter in teks_tanpa_padding:

        # Base64 character → nilai 0-63
        nilai = tabel_base64.index(karakter)

        # Nilai → 6-bit
        bit = format(nilai, "06b")

        semua_bit += bit

        proses.append({
            "Karakter Base64": karakter,
            "Nilai": nilai,
            "6-bit": bit
        })

    # Buang bit padding yang bukan bagian dari data
    jumlah_byte = len(teks_tanpa_padding) * 6 // 8
    jumlah_bit_data = jumlah_byte * 8

    bit_data = semua_bit[:jumlah_bit_data]

    # 8-bit → byte
    byte_hasil = []

    for i in range(0, len(bit_data), 8):

        kelompok_bit = bit_data[i:i+8]

        byte = int(kelompok_bit, 2)

        byte_hasil.append(byte)

    return byte_hasil, proses

def tampilkan_karakter(karakter):
    kode = ord(karakter)
    bisa_dicetak = 32 <= kode <= 126
    if bisa_dicetak:
        return karakter
    return f"(0x{kode:02X})"

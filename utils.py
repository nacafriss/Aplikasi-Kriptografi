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


def tampilkan_karakter(karakter):
    kode = ord(karakter)
    bisa_dicetak = 32 <= kode <= 126
    if bisa_dicetak:
        return karakter
    return f"(0x{kode:02X})"

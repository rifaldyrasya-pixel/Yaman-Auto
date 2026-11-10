"""
file_handler.py
Modul pengelola FILE EKSTERNAL (format CSV sederhana di folder data/).
Halaman 14 flowchart: baca_file() dan simpan_file().
"""
import os

# Semua file data disimpan di folder "data" di samping program
FOLDER_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FILE_USER = os.path.join(FOLDER_DATA, "users.txt")
FILE_INV = os.path.join(FOLDER_DATA, "inventaris.txt")
FILE_ANTREAN = os.path.join(FOLDER_DATA, "antrean.txt")
FILE_TRANSAKSI = os.path.join(FOLDER_DATA, "transaksi.txt")


def baca_file(nama_file):
    """Membaca file -> list of list. Jika file belum ada, dibuat kosong."""
    os.makedirs(os.path.dirname(nama_file), exist_ok=True)

    if not os.path.exists(nama_file):
        with open(nama_file, "w", encoding="utf-8"):
            pass
        return []

    data = []
    with open(nama_file, "r", encoding="utf-8") as f:
        for baris in f:
            baris = baris.strip()
            if baris:
                data.append(baris.split(","))
    return data


def simpan_file(nama_file, data):
    """Menyimpan list of list ke file (menimpa isi lama)."""
    os.makedirs(os.path.dirname(nama_file), exist_ok=True)
    with open(nama_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(",".join(str(x) for x in item) + "\n")


def ambil_item(data, nomor):
    """Ambil item berdasarkan nomor urut (mulai dari 1). None jika tidak ada.
    Yang dikembalikan adalah list aslinya, jadi perubahan langsung ikut ke data."""
    for no, item in enumerate(data, start=1):
        if no == nomor:
            return item
    return None
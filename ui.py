import os
import sys

# Mengaktifkan warna ANSI di terminal Windows
os.system("")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RESET = "\033[0m"
BOLD = "\033[1m"
MERAH = "\033[91m"
HIJAU = "\033[92m"
KUNING = "\033[93m"
BIRU = "\033[94m"
UNGU = "\033[95m"
CYAN = "\033[96m"
ABU = "\033[90m"

LEBAR = 90


def warna(teks, kode):
    return f"{kode}{teks}{RESET}"


def bersih():
    os.system("cls" if os.name == "nt" else "clear")


def garis(char="═", kode=CYAN):
    print(warna(char * LEBAR, kode))


def banner():
    """Logo kelompok Yaman Auto."""
    print(warna(r"""
   __   __     _       __  __      _       _   _
   \ \ / /    / \     |  \/  |    / \     | \ | |
    \ V /    / _ \    | |\/| |   / _ \    |  \| |
     | |    / ___ \   | |  | |  / ___ \   | |\  |
     |_|   /_/   \_\  |_|  |_| /_/   \_\  |_| \_|
""", KUNING))
    print(warna(r"""      _       _   _   _____    ___
     / \     | | | | |_   _|  / _ \
    / _ \    | | | |   | |   | | | |
   / ___ \   | |_| |   | |   | |_| |
  /_/   \_\   \___/    |_|    \___/
""", CYAN))
    print(warna("Sistem Inventaris & Antrean Servis Bengkel Motor".center(LEBAR), ABU))


def judul(teks, kode=CYAN):
    """Kotak judul."""
    print()
    print(warna("╔" + "═" * (LEBAR - 2) + "╗", kode))
    print(warna("║", kode) + warna(teks.upper().center(LEBAR - 2), BOLD + kode) + warna("║", kode))
    print(warna("╚" + "═" * (LEBAR - 2) + "╝", kode))


def menu(daftar, kode=CYAN):
    """daftar = list of (nomor, label)."""
    for nomor, label in daftar:
        print(f"  {warna('[' + str(nomor) + ']', kode + BOLD)} {label}")
    print(warna("─" * LEBAR, ABU))


def sukses(teks):
    print(warna(f"\n  ✔ {teks}", HIJAU + BOLD))


def gagal(teks):
    print(warna(f"\n  ✘ {teks}", MERAH + BOLD))


def info(teks):
    print(warna(f"\n  ℹ {teks}", KUNING))


def tanya(teks):
    return input(warna(f"  ➤ {teks}", BIRU)).strip()


def jeda(teks="Tekan Enter untuk melanjutkan..."):
    input(warna(f"\n  {teks}", ABU))


def potong(teks, lebar):
    teks = str(teks)
    return teks if len(teks) <= lebar else teks[: lebar - 1] + "…"


def rupiah(angka):
    return "Rp " + f"{int(angka):,}".replace(",", ".")


def warna_status(status):
    peta = {"Menunggu": KUNING, "Dikerjakan": BIRU, "Selesai": HIJAU}
    return peta.get(status, RESET)


def bersihkan_koma(teks):
    """Koma dihapus karena file disimpan dengan pemisah koma."""
    return " ".join(teks.replace(",", " ").split())


def ke_angka(teks, nama="Input"):
    """Ubah teks jadi bilangan bulat >= 0. Titik pemisah ribuan (50.000) diperbolehkan."""
    bersih_teks = teks.replace(".", "").replace(" ", "")
    if not bersih_teks.isdigit():
        raise ValueError(f"{nama} harus berupa angka bulat positif!")
    return int(bersih_teks)


def tanya_nomor(teks, jumlah):
    """Minta nomor urut 1..jumlah. Melempar ValueError jika tidak valid."""
    nomor = ke_angka(tanya(teks), "Nomor")
    if not 1 <= nomor <= jumlah:
        raise ValueError(f"Nomor harus antara 1 sampai {jumlah}!")
    return nomor

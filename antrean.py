"""
antrean.py
Halaman 9-13 flowchart: CRUD antrean servis.
Format antrean.txt :
  id, akun, nama, plat, motor, keluhan, status, biaya, pembayaran
  (akun = username pemilik, '-' jika didaftarkan admin untuk pelanggan langsung)
Status     : Menunggu / Dikerjakan / Selesai
Pembayaran : Belum / Lunas
"""
import re
from file_handler import baca_file, simpan_file, ambil_item, FILE_ANTREAN
from auth import ambil_nama
import ui

# Posisi kolom supaya kode mudah dibaca
ID, AKUN, NAMA, PLAT, MOTOR, KELUHAN, STATUS, BIAYA, BAYAR = range(9)
DAFTAR_STATUS = {"1": "Menunggu", "2": "Dikerjakan", "3": "Selesai"}


def baca_antrean():
    """Baca antrean. Data format lama (5 kolom) otomatis disesuaikan."""
    hasil = []
    for d in baca_file(FILE_ANTREAN):
        if len(d) == 5:   # lama: id,pelanggan,motor,keluhan,status
            d = [d[0], d[1], d[1], "-", d[2], d[3], d[4], "0", "Belum"]
        if len(d) == 9:
            hasil.append(d)
    return hasil


def rapikan_plat(teks):
    """'kt1234ab' / 'KT 1234 AB' -> 'KT 1234 AB'. ValueError jika format salah."""
    mentah = teks.upper().replace(" ", "").replace(",", "")
    cocok = re.fullmatch(r"([A-Z]{1,2})(\d{1,4})([A-Z]{0,3})", mentah)
    if not cocok:
        raise ValueError("Format plat tidak valid! Contoh: KT 1234 AB")
    return " ".join(bagian for bagian in cocok.groups() if bagian)


def _plat_masih_antre(data, plat, kecuali=None):
    """True jika plat itu masih punya antrean yang belum Selesai."""
    return any(d[PLAT] == plat and d[STATUS] != "Selesai" and d is not kecuali for d in data)


def _id_baru(data):
    """ID unik: nomor terbesar + 1 (aman walau ada antrean yang dihapus)."""
    terbesar = 0
    for d in data:
        try:
            terbesar = max(terbesar, int(d[ID].split("-")[1]))
        except (IndexError, ValueError):
            pass
    return f"ANT-{terbesar + 1:03d}"


def _teks_biaya(item):
    if int(item[BIAYA]) == 0:
        return ui.warna(f"{'-':<12}", ui.ABU)
    lunas = item[BAYAR] == "Lunas"
    teks = ui.rupiah(item[BIAYA]) + (" ✓" if lunas else "")
    return ui.warna(f"{teks:<12}", ui.HIJAU if lunas else ui.KUNING)


def lihat_antrean(username_login="", role="admin"):
    """READ - admin melihat semua antrean, pelanggan hanya miliknya sendiri."""
    data = baca_antrean()
    judul = "Daftar Antrean Servis" if role == "admin" else "Antrean Servis Saya"
    ui.judul(judul, ui.BIRU)
    print(ui.warna(f"  {'NO':<4}{'ID':<9}{'PEMILIK':<13}{'PLAT':<12}{'MOTOR':<13}"
                   f"{'KELUHAN':<14}{'STATUS':<11}{'BIAYA':<12}", ui.BOLD + ui.KUNING))
    ui.garis("─", ui.ABU)

    tampil = data if role == "admin" else [d for d in data if d[AKUN] == username_login]

    if not tampil:
        print(ui.warna("  -- Belum ada antrean servis --".center(ui.LEBAR), ui.ABU))
    else:
        for no, item in enumerate(tampil, start=1):
            print(
                f"  {no:<4}{item[ID]:<9}"
                f"{ui.potong(item[NAMA], 12):<13}"
                f"{ui.potong(item[PLAT], 11):<12}"
                f"{ui.potong(item[MOTOR], 12):<13}"
                f"{ui.potong(item[KELUHAN], 13):<14}"
                f"{ui.warna(f'{item[STATUS]:<11}', ui.warna_status(item[STATUS]) + ui.BOLD)}"
                f"{_teks_biaya(item)}"
            )
    ui.garis("=", ui.CYAN)
    print(ui.warna("  Biaya kuning = belum dibayar, hijau ✓ = lunas", ui.ABU))


def daftar_antrean_baru(username_login, role):
    """CREATE - daftarkan motor yang masuk (dengan nama pemilik dan plat nomor)."""
    ui.bersih()
    ui.judul("Pendaftaran Antrean Servis", ui.BIRU)
    data = baca_antrean()

    try:
        if role == "admin":
            akun = "-"
            nama_pelanggan = ui.bersihkan_koma(ui.tanya("Nama Pemilik Motor : "))
            if not nama_pelanggan:
                raise ValueError("Nama pemilik wajib diisi!")
        else:
            akun = username_login
            nama_pelanggan = ambil_nama(username_login)
            print(f"  Nama Pemilik       : {ui.warna(nama_pelanggan, ui.BOLD)}")

        plat = rapikan_plat(ui.tanya("Plat Nomor (KT 1234 AB) : "))
        if _plat_masih_antre(data, plat):
            raise ValueError(f"Motor {plat} masih ada di antrean dan belum selesai!")
        motor = ui.bersihkan_koma(ui.tanya("Merk & Tipe Motor : "))
        keluhan = ui.bersihkan_koma(ui.tanya("Keluhan / Servis  : "))
        if not motor or not keluhan:
            raise ValueError("Data Motor dan Keluhan wajib diisi!")
    except ValueError as e:
        ui.gagal(f"Error Pendaftaran: {e}")
        ui.jeda()
        return

    id_antrean = _id_baru(data)
    status_awal = "Menunggu"
    data.append([id_antrean, akun, nama_pelanggan, plat, motor, keluhan, status_awal, "0", "Belum"])
    simpan_file(FILE_ANTREAN, data)

    ui.sukses("Pendaftaran Antrean Berhasil!")
    print(f"  ID Antrean : {ui.warna(id_antrean, ui.BOLD)}")
    print(f"  Pemilik    : {nama_pelanggan}  ({plat})")
    print(f"  Status     : {ui.warna(status_awal, ui.warna_status(status_awal) + ui.BOLD)}")
    ui.jeda()


def ubah_data_antrean():
    """UPDATE - admin mengubah data antrean (nama, plat, motor, keluhan, status, biaya)."""
    ui.bersih()
    data = baca_antrean()
    lihat_antrean(role="admin")
    if not data:
        ui.jeda()
        return

    try:
        nomor = ui.tanya_nomor("\n  Pilih NOMOR antrean yang diubah : ", len(data))
    except ValueError as e:
        ui.gagal(str(e))
        ui.jeda()
        return

    item = ambil_item(data, nomor)
    ui.info(f"Mengubah {item[ID]}. Kosongkan input (Enter) jika tidak ingin mengubah.")
    try:
        nama_baru = ui.bersihkan_koma(ui.tanya(f"Nama pemilik [{item[NAMA]}] : ")) or item[NAMA]

        plat_teks = ui.tanya(f"Plat nomor   [{item[PLAT]}] : ")
        plat_baru = rapikan_plat(plat_teks) if plat_teks else item[PLAT]
        if plat_baru != item[PLAT] and _plat_masih_antre(data, plat_baru, kecuali=item):
            raise ValueError(f"Plat {plat_baru} sudah ada di antrean lain!")

        motor_baru = ui.bersihkan_koma(ui.tanya(f"Motor        [{item[MOTOR]}] : ")) or item[MOTOR]
        keluhan_baru = ui.bersihkan_koma(ui.tanya(f"Keluhan      [{item[KELUHAN]}] : ")) or item[KELUHAN]

        print(ui.warna(f"  Status sekarang: {item[STATUS]}", ui.ABU))
        ui.menu([(1, "Menunggu"), (2, "Dikerjakan"), (3, "Selesai")], ui.BIRU)
        status_pilih = ui.tanya("Status baru (1-3, Enter = tetap) : ")
        if status_pilih and status_pilih not in DAFTAR_STATUS:
            raise ValueError("Pilihan status tidak valid!")
        status_baru = DAFTAR_STATUS.get(status_pilih, item[STATUS])

        biaya_baru = item[BIAYA]
        if item[BAYAR] == "Lunas":
            ui.info("Servis ini sudah lunas, biaya tidak bisa diubah.")
        else:
            biaya_teks = ui.tanya(f"Biaya servis (Rp) [{ui.rupiah(item[BIAYA])}] : ")
            if biaya_teks:
                biaya_baru = str(ui.ke_angka(biaya_teks, "Biaya"))

        # semua input valid -> baru disimpan
        item[NAMA], item[PLAT] = nama_baru, plat_baru
        item[MOTOR], item[KELUHAN] = motor_baru, keluhan_baru
        item[STATUS], item[BIAYA] = status_baru, biaya_baru
        simpan_file(FILE_ANTREAN, data)
        ui.sukses("Data antrean berhasil diperbarui!")
    except ValueError as e:
        ui.gagal(f"Error: {e}")
    ui.jeda()


def hapus_antrean():
    """DELETE - admin menghapus antrean."""
    ui.bersih()
    data = baca_antrean()
    lihat_antrean(role="admin")
    if not data:
        ui.jeda()
        return

    try:
        nomor = ui.tanya_nomor("\n  Pilih NOMOR antrean yang dihapus : ", len(data))
    except ValueError as e:
        ui.gagal(str(e))
        ui.jeda()
        return

    antrean_dihapus = ambil_item(data, nomor)
    yakin = ui.tanya(f"Yakin hapus {antrean_dihapus[ID]} ({antrean_dihapus[NAMA]})? (y/n) : ").lower()
    if yakin == "y":
        data.remove(antrean_dihapus)
        simpan_file(FILE_ANTREAN, data)
        ui.sukses(f"Antrean milik {antrean_dihapus[NAMA]} berhasil dihapus!")
    else:
        ui.info("Penghapusan dibatalkan.")
    ui.jeda()


def menu_antrean(username_login, role):
    """Menu antrean. Opsi 3 & 4 hanya untuk admin."""
    while True:
        ui.bersih()
        ui.judul("Menu Antrean Servis", ui.BIRU)
        opsi = [(1, "Lihat Antrean"), (2, "Daftar Antrean Baru")]
        if role == "admin":
            opsi += [(3, "Ubah Data Antrean"), (4, "Hapus Antrean")]
        opsi.append((0, "Kembali"))
        ui.menu(opsi, ui.BIRU)
        pilihan = ui.tanya("Pilih menu : ")

        if pilihan == "1":
            ui.bersih()
            lihat_antrean(username_login, role)
            ui.jeda()
        elif pilihan == "2":
            daftar_antrean_baru(username_login, role)
        elif pilihan == "3" and role == "admin":
            ubah_data_antrean()
        elif pilihan == "4" and role == "admin":
            hapus_antrean()
        elif pilihan == "0":
            break
        else:
            ui.gagal("Pilihan tidak valid atau akses ditolak.")
            ui.jeda()
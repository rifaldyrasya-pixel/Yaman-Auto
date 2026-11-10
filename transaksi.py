"""
transaksi.py
Sistem pembayaran:
  - Beli sparepart (pelanggan tidak harus servis)  -> stok otomatis berkurang
  - Bayar biaya servis (status Selesai, biaya sudah diisi admin)
  - Riwayat transaksi
Format transaksi.txt : id, waktu, akun, nama, jenis, keterangan, total, bayar, kembalian
"""
from datetime import datetime
from file_handler import baca_file, simpan_file, ambil_item, FILE_INV, FILE_TRANSAKSI, FILE_ANTREAN
from inventaris import lihat_inventaris
from antrean import baca_antrean, ID, AKUN, NAMA, PLAT, MOTOR, STATUS, BIAYA, BAYAR
from auth import ambil_nama
import ui


def _catat_transaksi(akun, nama, jenis, keterangan, total, bayar):
    data = baca_file(FILE_TRANSAKSI)
    id_trx = f"TRX-{len(data) + 1:03d}"
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M")
    kembalian = bayar - total
    data.append([id_trx, waktu, akun, nama, jenis, ui.bersihkan_koma(keterangan),
                 str(total), str(bayar), str(kembalian)])
    simpan_file(FILE_TRANSAKSI, data)
    return id_trx, waktu, kembalian


def _minta_bayar(total):
    """Tampilkan total, minta uang bayar. ValueError jika uang kurang."""
    print(f"\n  Total Bayar       : {ui.warna(ui.rupiah(total), ui.BOLD + ui.KUNING)}")
    bayar = ui.ke_angka(ui.tanya("Uang Dibayar (Rp) : "), "Uang bayar")
    if bayar < total:
        raise ValueError(f"Uang kurang {ui.rupiah(total - bayar)}! Pembayaran dibatalkan.")
    return bayar


def _cetak_struk(id_trx, waktu, nama, keterangan, total, bayar, kembalian):
    print(ui.warna("\n  ┌" + "─" * 44 + "┐", ui.HIJAU))
    print(ui.warna("  │" + "STRUK PEMBAYARAN - YAMAN AUTO".center(44) + "│", ui.HIJAU + ui.BOLD))
    print(ui.warna("  └" + "─" * 44 + "┘", ui.HIJAU))
    print(f"  No. Transaksi : {id_trx}")
    print(f"  Waktu         : {waktu}")
    print(f"  Nama          : {nama}")
    print(f"  Keterangan    : {keterangan}")
    print(f"  Total         : {ui.rupiah(total)}")
    print(f"  Dibayar       : {ui.rupiah(bayar)}")
    print(f"  Kembalian     : {ui.warna(ui.rupiah(kembalian), ui.BOLD + ui.HIJAU)}")


def beli_sparepart(username, role):
    """Beli sparepart/oli tanpa harus servis. Stok otomatis berkurang."""
    ui.bersih()
    data = baca_file(FILE_INV)
    lihat_inventaris()
    if not data:
        ui.jeda()
        return

    if role == "admin":
        akun = "-"
        nama = ui.bersihkan_koma(ui.tanya("\n  Nama Pembeli (Enter = Umum) : ")) or "Umum"
    else:
        akun = username
        nama = ambil_nama(username)

    try:
        nomor = ui.tanya_nomor("  Pilih NOMOR barang : ", len(data))
        item = ambil_item(data, nomor)
        stok = int(item[2])
        if stok == 0:
            raise ValueError(f"Stok {item[1]} sedang habis!")

        jumlah = ui.ke_angka(ui.tanya(f"  Jumlah beli (stok {stok}) : "), "Jumlah")
        if jumlah < 1:
            raise ValueError("Jumlah minimal 1!")
        if jumlah > stok:
            raise ValueError(f"Stok tidak cukup! Sisa stok hanya {stok}.")

        total = int(item[3]) * jumlah
        bayar = _minta_bayar(total)

        item[2] = str(stok - jumlah)          # stok otomatis berkurang
        simpan_file(FILE_INV, data)
        keterangan = f"{item[1]} x{jumlah}"
        id_trx, waktu, kembalian = _catat_transaksi(akun, nama, "Sparepart", keterangan, total, bayar)
        ui.sukses("Pembayaran berhasil!")
        _cetak_struk(id_trx, waktu, nama, keterangan, total, bayar, kembalian)
    except ValueError as e:
        ui.gagal(f"Pembelian Gagal: {e}")
    ui.jeda()


def bayar_servis(username, role):
    """Bayar biaya servis. Syarat: status Selesai dan biaya sudah diisi admin."""
    ui.bersih()
    ui.judul("Pembayaran Servis", ui.KUNING)
    antrean = baca_antrean()
    layak = [d for d in antrean
             if d[STATUS] == "Selesai" and int(d[BIAYA]) > 0 and d[BAYAR] != "Lunas"
             and (role == "admin" or d[AKUN] == username)]

    if not layak:
        ui.info("Tidak ada servis yang perlu dibayar.")
        print(ui.warna("  (Servis harus berstatus Selesai dan biayanya sudah diisi admin)", ui.ABU))
        ui.jeda()
        return

    print(ui.warna(f"  {'NO':<4}{'ID':<9}{'PEMILIK':<16}{'PLAT':<13}{'MOTOR':<16}{'BIAYA':>14}",
                   ui.BOLD + ui.KUNING))
    ui.garis("─", ui.ABU)
    for no, d in enumerate(layak, start=1):
        print(f"  {no:<4}{d[ID]:<9}{ui.potong(d[NAMA], 15):<16}{d[PLAT]:<13}"
              f"{ui.potong(d[MOTOR], 15):<16}{ui.rupiah(d[BIAYA]):>14}")
    ui.garis("=", ui.CYAN)

    try:
        nomor = ui.tanya_nomor("\n  Pilih NOMOR servis yang dibayar : ", len(layak))
        item = ambil_item(layak, nomor)
        total = int(item[BIAYA])
        bayar = _minta_bayar(total)

        item[BAYAR] = "Lunas"
        simpan_file(FILE_ANTREAN, antrean)
        keterangan = f"Servis {item[ID]} {item[PLAT]}"
        id_trx, waktu, kembalian = _catat_transaksi(item[AKUN], item[NAMA], "Servis", keterangan, total, bayar)
        ui.sukses("Pembayaran servis berhasil! Status: LUNAS")
        _cetak_struk(id_trx, waktu, item[NAMA], keterangan, total, bayar, kembalian)
    except ValueError as e:
        ui.gagal(f"Pembayaran Gagal: {e}")
    ui.jeda()


def lihat_transaksi(username, role):
    """Admin melihat semua transaksi, pelanggan hanya miliknya."""
    data = baca_file(FILE_TRANSAKSI)
    ui.judul("Riwayat Transaksi" if role != "admin" else "Riwayat Semua Transaksi", ui.UNGU)
    print(ui.warna(f"  {'NO':<4}{'ID':<9}{'WAKTU':<17}{'NAMA':<13}{'JENIS':<11}{'KETERANGAN':<20}{'TOTAL':>12}",
                   ui.BOLD + ui.KUNING))
    ui.garis("─", ui.ABU)

    tampil = data if role == "admin" else [d for d in data if d[2] == username]
    if not tampil:
        print(ui.warna("  -- Belum ada transaksi --".center(ui.LEBAR), ui.ABU))
    else:
        pendapatan = 0
        for no, d in enumerate(tampil, start=1):
            pendapatan += int(d[6])
            print(f"  {no:<4}{d[0]:<9}{d[1]:<17}{ui.potong(d[3], 12):<13}{d[4]:<11}"
                  f"{ui.potong(d[5], 19):<20}{ui.rupiah(d[6]):>12}")
        ui.garis("─", ui.ABU)
        label = "Total Pendapatan" if role == "admin" else "Total Pengeluaran"
        print(f"  {label}: {ui.warna(ui.rupiah(pendapatan), ui.BOLD + ui.HIJAU)}")
    ui.garis("=", ui.CYAN)


def menu_transaksi(username, role):
    while True:
        ui.bersih()
        ui.judul("Transaksi & Pembayaran", ui.KUNING)
        if role == "admin":
            ui.menu([(1, "Jual Sparepart (Kasir)"), (2, "Terima Pembayaran Servis"),
                     (3, "Riwayat Semua Transaksi"), (0, "Kembali")], ui.KUNING)
        else:
            ui.menu([(1, "Beli Sparepart"), (2, "Bayar Servis"),
                     (3, "Riwayat Transaksi Saya"), (0, "Kembali")], ui.KUNING)
        pilihan = ui.tanya("Pilih menu (0-3) : ")

        if pilihan == "1":
            beli_sparepart(username, role)
        elif pilihan == "2":
            bayar_servis(username, role)
        elif pilihan == "3":
            ui.bersih()
            lihat_transaksi(username, role)
            ui.jeda()
        elif pilihan == "0":
            break
        else:
            ui.gagal("Pilihan tidak valid.")
            ui.jeda()
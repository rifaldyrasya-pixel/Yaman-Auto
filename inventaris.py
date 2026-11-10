"""
inventaris.py
Halaman 4-8 flowchart: CRUD stok sparepart & oli.
Format inventaris.txt : kode,nama,stok,harga
Kode barang DIBUAT OTOMATIS oleh program (contoh: OLI-001), bukan diketik admin.
"""
import re
from file_handler import baca_file, simpan_file, ambil_item, FILE_INV
import ui

STOK_MENIPIS = 5  # stok <= 5 ditandai merah


def buat_kode_barang(nama, data):
    """3 huruf pertama nama + nomor urut berikutnya. Contoh: 'Oli MPX2' -> OLI-003."""
    huruf = re.sub(r"[^A-Za-z]", "", nama).upper()
    prefix = huruf[:3].ljust(3, "X") if huruf else "BRG"

    terbesar = 0
    for item in data:
        cocok = re.search(r"(\d+)$", item[0])
        if cocok:
            terbesar = max(terbesar, int(cocok.group(1)))
    return f"{prefix}-{terbesar + 1:03d}"


def lihat_inventaris():
    """READ - tampilkan semua barang."""
    data = baca_file(FILE_INV)
    ui.judul("Data Stok Inventaris", ui.HIJAU)
    print(ui.warna(f"  {'NO':<5}{'KODE':<11}{'NAMA BARANG':<32}{'STOK':>8}{'HARGA':>18}",
                   ui.BOLD + ui.KUNING))
    ui.garis("─", ui.ABU)

    if not data:
        print(ui.warna("  -- Data Stok Masih Kosong --".center(ui.LEBAR), ui.ABU))
    else:
        for no, item in enumerate(data, start=1):
            stok = int(item[2])
            teks_stok = "HABIS" if stok == 0 else str(stok)
            warna_stok = ui.MERAH if stok <= STOK_MENIPIS else ui.HIJAU
            print(
                f"  {no:<5}{ui.potong(item[0], 10):<11}"
                f"{ui.potong(item[1], 31):<32}"
                + ui.warna(f"{teks_stok:>8}", warna_stok)
                + f"{ui.rupiah(item[3]):>18}"
            )
    ui.garis("=", ui.CYAN)
    if data:
        print(ui.warna(f"  Stok merah = menipis (<= {STOK_MENIPIS})", ui.ABU))


def tambah_barang():
    """CREATE - barang baru dari supplier. Kode dibuat otomatis."""
    ui.bersih()
    ui.judul("Tambah Barang Baru", ui.HIJAU)
    data = baca_file(FILE_INV)
    try:
        nama = ui.bersihkan_koma(ui.tanya("Nama Sparepart/Oli : "))
        if not nama:
            raise ValueError("Nama barang tidak boleh kosong!")
        if any(item[1].lower() == nama.lower() for item in data):
            raise ValueError("Barang itu sudah ada! Gunakan menu Ubah untuk mengganti stok.")

        kode_baru = buat_kode_barang(nama, data)      # variabel penyimpan kode otomatis
        print(f"  Kode Barang        : {ui.warna(kode_baru, ui.BOLD + ui.HIJAU)}  (otomatis)")

        stok = ui.ke_angka(ui.tanya("Jumlah Stok        : "), "Stok")
        harga = ui.ke_angka(ui.tanya("Harga Satuan (Rp)  : "), "Harga")

        data.append([kode_baru, nama, str(stok), str(harga)])
        simpan_file(FILE_INV, data)
        ui.sukses(f"Barang {kode_baru} berhasil ditambahkan!")
    except ValueError as e:
        ui.gagal(f"Gagal Menambah Barang: {e}")
    finally:
        ui.jeda("Tekan Enter untuk kembali...")


def ubah_barang():
    """UPDATE - koreksi data / harga berubah / stok berubah. Pilih barang lewat NOMOR."""
    ui.bersih()
    data = baca_file(FILE_INV)
    lihat_inventaris()
    if not data:
        ui.jeda()
        return

    try:
        pilihan = ui.tanya_nomor("\n  Pilih NOMOR barang yang diubah : ", len(data))
    except ValueError as e:
        ui.gagal(str(e))
        ui.jeda()
        return

    for no, item in enumerate(data, start=1):
        if no == pilihan:
            ui.info(f"Mengubah {item[0]}. Kosongkan input (Enter) jika tidak ingin mengubah.")
            print(f"  Data lama -> {item[1]} | stok {item[2]} | {ui.rupiah(item[3])}")
            try:
                nama_baru = ui.bersihkan_koma(ui.tanya("Nama baru  : ")) or item[1]
                stok_teks = ui.tanya("Stok baru  : ")
                harga_teks = ui.tanya("Harga baru : ")
                stok_baru = ui.ke_angka(stok_teks, "Stok") if stok_teks else int(item[2])
                harga_baru = ui.ke_angka(harga_teks, "Harga") if harga_teks else int(item[3])

                item[1] = nama_baru
                item[2] = str(stok_baru)
                item[3] = str(harga_baru)
                simpan_file(FILE_INV, data)
                ui.sukses("Data barang berhasil diperbarui!")
            except ValueError as e:
                ui.gagal(f"Error: {e}")
            break
    ui.jeda()


def hapus_barang():
    """DELETE - barang yang sudah tidak dijual. Pilih barang lewat NOMOR."""
    ui.bersih()
    data = baca_file(FILE_INV)
    lihat_inventaris()
    if not data:
        ui.jeda()
        return

    try:
        pilihan = ui.tanya_nomor("\n  Pilih NOMOR barang yang dihapus : ", len(data))
    except ValueError as e:
        ui.gagal(str(e))
        ui.jeda()
        return

    item = ambil_item(data, pilihan)
    yakin = ui.tanya(f"Yakin hapus {item[0]} - {item[1]}? (y/n) : ").lower()
    if yakin == "y":
        data_baru = [x for x in data if x[0] != item[0]]
        simpan_file(FILE_INV, data_baru)
        ui.sukses("Barang berhasil dihapus dari daftar!")
    else:
        ui.info("Penghapusan dibatalkan.")
    ui.jeda()


def menu_inventaris_admin():
    """Menu CRUD inventaris khusus admin."""
    while True:
        ui.bersih()
        ui.judul("Kelola Inventaris", ui.HIJAU)
        ui.menu([(1, "Lihat Stok"), (2, "Tambah Barang"), (3, "Ubah Barang"),
                 (4, "Hapus Barang"), (0, "Kembali")], ui.HIJAU)
        pilihan = ui.tanya("Pilih menu (0-4) : ")

        if pilihan == "1":
            ui.bersih()
            lihat_inventaris()
            ui.jeda()
        elif pilihan == "2":
            tambah_barang()
        elif pilihan == "3":
            ubah_barang()
        elif pilihan == "4":
            hapus_barang()
        elif pilihan == "0":
            break
        else:
            ui.gagal("Pilihan tidak valid.")
            ui.jeda()
import os
from file_handler import baca_file, simpan_file

FILE_INV = "inventaris.txt"


def lihat_inventaris():
  data = baca_file(FILE_INV)
  print("\n" + "=" * 60)
  print(f"{'KODE':<8} | {'NAMA BARANG':<25} | {'STOK':<8} | {'HARGA (Rp)'}")
  print("=" * 60)
  if not data:
    print("            -- Data Stok Masih Kosong --")
  else:
    for item in data:
      # Modul 6 & 2: Output Terformat
      print(f"{item[0]:<8} | {item[1]:<25} | {item[2]:<8} | Rp {int(item[3]):,}")
  print("=" * 60)


def tambah_barang():
  os.system("cls" if os.name == "nt" else "clear")
  print("--- TAMBAH STOK BARANG BARU (ADMIN) ---")
  data = baca_file(FILE_INV)

  kode = input("Masukkan Kode Barang (cth: SP01) : ").strip().upper()
  nama = input("Masukkan Nama Sparepart/Oli      : ").strip()

  # Error Handling Input Angka (Modul 7.2)
  try:
    if not kode or not nama:
      raise ValueError("Kode dan Nama barang tidak boleh kosong!")

    # Cek duplikasi kode barang
    for item in data:
      if item[0] == kode:
        raise ValueError(
            f"Kode barang '{kode}' sudah ada di inventaris! Gunakan menu edit."
        )

    stok = int(input("Masukkan Jumlah Stok (Angka)     : "))
    harga = int(input("Masukkan Harga Satuan (Rp)       : "))

    if stok < 0 or harga < 0:
      raise ValueError("Stok dan harga tidak boleh bernilai negatif!")

    data.append([kode, nama, str(stok), str(harga)])
    simpan_file(FILE_INV, data)
    print(f"\n✅ Barang '{nama}' berhasil ditambahkan ke inventaris!")

  except ValueError as e:
    print(f"\n❌ Gagal Menambah Barang: {e}")

  finally:
    input("\nTekan Enter untuk kembali...")


def ubah_barang():
  os.system("cls" if os.name == "nt" else "clear")
  print("--- UBAH DATA STOK / HARGA BARANG ---")
  data = baca_file(FILE_INV)
  lihat_inventaris()

  if not data:
    input("\nTekan Enter...")
    return

  target_kode = input("\nMasukkan KODE barang yang ingin diubah: ").strip().upper()
  ditemukan = False

  for i in range(len(data)):
    if data[i][0] == target_kode:
      ditemukan = True
      print(f"\nData Lama: {data[i][1]} | Stok: {data[i][2]} | Harga: Rp{data[i][3]}")
      nama_baru = input(f"Nama Baru [{data[i][1]}]: ").strip() or data[i][1]
      
      try:
        stok_input = input(f"Stok Baru [{data[i][2]}]: ").strip()
        harga_input = input(f"Harga Baru [{data[i][3]}]: ").strip()

        stok_baru = int(stok_input) if stok_input else int(data[i][2])
        harga_baru = int(harga_input) if harga_input else int(data[i][3])

        data[i][1] = nama_baru
        data[i][2] = str(stok_baru)
        data[i][3] = str(harga_baru)

        simpan_file(FILE_INV, data)
        print("\n✅ Data barang berhasil diperbarui!")

      except ValueError:
        print("\n❌ Error: Stok dan harga harus berupa angka valid!")
      break

  if not ditemukan:
    print(f"\n❌ Kode barang '{target_kode}' tidak ditemukan.")

  input("\nTekan Enter...")


def hapus_barang():
  os.system("cls" if os.name == "nt" else "clear")
  print("--- HAPUS BARANG DARI INVENTARIS ---")
  data = baca_file(FILE_INV)
  lihat_inventaris()

  if not data:
    input("\nTekan Enter...")
    return

  target_kode = input("\nMasukkan KODE barang yang akan dihapus: ").strip().upper()
  data_baru = [item for item in data if item[0] != target_kode]

  if len(data_baru) < len(data):
    simpan_file(FILE_INV, data_baru)
    print(f"\n✅ Barang dengan kode '{target_kode}' berhasil dihapus.")
  else:
    print(f"\n❌ Kode barang '{target_kode}' tidak ditemukan.")

  input("\nTekan Enter...")


def menu_inventaris_admin():
  while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 55)
    print("      MANAJEMEN INVENTARIS BENGKEL - YAMAN AUTO       ")
    print("=" * 55)
    print("[1] Lihat Stok Sparepart & Oli")
    print("[2] Tambah Barang Baru")
    print("[3] Ubah Data Barang (Stok/Harga)")
    print("[4] Hapus Barang dari Sistem")
    print("[0] Kembali ke Menu Utama")
    print("-" * 55)

    pilihan = input("Pilih menu (0-4): ").strip()
    if pilihan == "1":
      os.system("cls" if os.name == "nt" else "clear")
      lihat_inventaris()
      input("\nTekan Enter untuk kembali...")
    elif pilihan == "2":
      tambah_barang()
    elif pilihan == "3":
      ubah_barang()
    elif pilihan == "4":
      hapus_barang()
    elif pilihan == "0":
      break
    else:
      print("❌ Pilihan tidak valid.")
      input("Tekan Enter...")
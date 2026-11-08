import os
from datetime import datetime
from file_handler import baca_file, simpan_file

FILE_ANTREAN = "antrean.txt"


def lihat_antrean(username_login=None, role="admin"):
  data = baca_file(FILE_ANTREAN)
  print("\n" + "=" * 70)
  print(
      f"{'NO':<4} | {'PELANGGAN':<12} | {'MOTOR':<12} | {'KELUHAN':<18} |"
      " {'STATUS'}"
  )
  print("=" * 70)

  if not data:
    print("               -- Belum ada antrean servis --")
  else:
    count = 0
    for item in data:
      count += 1
      print(
          f"{count:<4} | {item[1]:<12} | {item[2]:<12} | {item[3]:<18} |"
          f" {item[4]}"
      )
  print("=" * 70)


def daftar_antrean_baru(username_login, role):
  os.system("cls" if os.name == "nt" else "clear")
  print("--- PENDAFTARAN ANTREAN SERVIS MOTOR ---")
  data = baca_file(FILE_ANTREAN)

  # Jika Admin, bisa mengetik nama pelanggan lain. Jika Pelanggan, otomatis nama akunnya.
  if role == "admin":
    nama_pelanggan = (
        input("Nama Pelanggan/Pemilik Motor : ").strip() or username_login
    )
  else:
    nama_pelanggan = username_login

  motor = input("Merk & Tipe Motor (cth: KLX 150) : ").strip()
  keluhan = input("Keluhan / Jenis Servis Motor  : ").strip()

  try:
    if not motor or not keluhan:
      raise ValueError("Data Motor dan Keluhan wajib diisi!")

    id_antrean = f"ANT-{len(data)+1:03d}"
    status_awal = "Menunggu"

    data.append([id_antrean, nama_pelanggan, motor, keluhan, status_awal])
    simpan_file(FILE_ANTREAN, data)

    print(
        f"\n✅ Pendaftaran Antrean Berhasil!"
        f"\nID Antrean : {id_antrean}"
        f"\nStatus     : [{status_awal}]"
    )

  except ValueError as e:
    print(f"\n❌ Error Pendaftaran: {e}")

  input("\nTekan Enter untuk kembali...")


def ubah_status_antrean():
  os.system("cls" if os.name == "nt" else "clear")
  print("--- UBAH STATUS ANTREAN SERVIS (ADMIN) ---")
  data = baca_file(FILE_ANTREAN)
  lihat_antrean(role="admin")

  if not data:
    input("\nTekan Enter...")
    return

  try:
    nomor = (
        int(input("\nMasukkan NOMOR urut antrean yang statusnya diubah: ")) - 1
    )
    if 0 <= nomor < len(data):
      print(f"\nMotor: {data[nomor][2]} (Pemilik: {data[nomor][1]})")
      print("Pilihan Status Baru:")
      print("[1] Menunggu")
      print("[2] Dikerjakan")
      print("[3] Selesai")

      pilihan = input("Pilih Status Baru (1-3): ").strip()
      status_dict = {"1": "Menunggu", "2": "Dikerjakan", "3": "Selesai"}

      if pilihan in status_dict:
        data[nomor][4] = status_dict[pilihan]
        simpan_file(FILE_ANTREAN, data)
        print(
            f"\n✅ Status antrean berhasil diperbarui menjadi [{status_dict[pilihan]}]!"
        )
      else:
        print("\n❌ Pilihan status tidak valid.")
    else:
      print("\n❌ Nomor antrean tidak ditemukan.")

  except ValueError:
    print("\n❌ Input harus berupa angka nomor urut!")

  input("\nTekan Enter...")


def hapus_antrean():
  os.system("cls" if os.name == "nt" else "clear")
  print("--- HAPUS DATA ANTREAN (ADMIN) ---")
  data = baca_file(FILE_ANTREAN)
  lihat_antrean(role="admin")

  if not data:
    input("\nTekan Enter...")
    return

  try:
    nomor = int(input("\nMasukkan NOMOR urut antrean yang akan dihapus: ")) - 1
    if 0 <= nomor < len(data):
      antrean_dihapus = data.pop(nomor)
      simpan_file(FILE_ANTREAN, data)
      print(f"\n✅ Antrean milik '{antrean_dihapus[1]}' berhasil dihapus.")
    else:
      print("\n❌ Nomor antrean tidak valid.")
  except ValueError:
    print("\n❌ Input harus berupa angka!")

  input("\nTekan Enter...")


def menu_antrean(username_login, role):
  while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 55)
    print("       MANAJEMEN ANTREAN SERVIS - YAMAN AUTO          ")
    print("=" * 55)
    print("[1] Lihat Daftar Antrean Servis")
    print("[2] Daftar Antrean Servis Baru")
    if role == "admin":
      print("[3] Ubah Status Servis (Menunggu -> Dikerjakan -> Selesai)")
      print("[4] Hapus Antrean")
    print("[0] Kembali ke Menu Utama")
    print("-" * 55)

    pilihan = input("Pilih menu: ").strip()

    if pilihan == "1":
      os.system("cls" if os.name == "nt" else "clear")
      lihat_antrean(username_login, role)
      input("\nTekan Enter untuk kembali...")
    elif pilihan == "2":
      daftar_antrean_baru(username_login, role)
    elif pilihan == "3" and role == "admin":
      ubah_status_antrean()
    elif pilihan == "4" and role == "admin":
      hapus_antrean()
    elif pilihan == "0":
      break
    else:
      print("❌ Pilihan tidak valid atau akses ditolak.")
      input("Tekan Enter...")
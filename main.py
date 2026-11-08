import os
from antrean import lihat_antrean, menu_antrean
from auth import login
from inventaris import lihat_inventaris, menu_inventaris_admin


def main():
  while True:
    user_session = login()

    # Jika memilih keluar di menu login
    if not user_session:
      os.system("cls" if os.name == "nt" else "clear")
      print("=" * 50)
      print(" Terima kasih telah menggunakan Sistem Yaman Auto! ")
      print("=" * 50)
      break

    username, role = user_session  # Unpacking Tuple (Modul 5)

    # Main Loop Aplikasi Berdasarkan Role
    while True:
      os.system("cls" if os.name == "nt" else "clear")
      print("=" * 60)
      print(f"    DASHBOARD SYSTEM YAMAN AUTO - [{role.upper()}]")
      print(f"    User Aktif: {username}")
      print("=" * 60)

      if role == "admin":
        print("[1] Kelola Inventaris (Stok Sparepart & Oli)")
        print("[2] Kelola Antrean Servis Motor")
        print("[0] Logout / Ganti Akun")
        print("=" * 60)

        pilihan = input("Pilih Menu (0-2): ").strip()
        if pilihan == "1":
          menu_inventaris_admin()
        elif pilihan == "2":
          menu_antrean(username, role)
        elif pilihan == "0":
          print("\nLogging out...")
          break
        else:
          print("❌ Pilihan tidak valid.")
          input("Tekan Enter...")

      else:  # Role Pelanggan / User
        print("[1] Daftar Antrean Servis Motor Baru")
        print("[2] Lihat Antrean & Status Motor Saya")
        print("[3] Lihat Katalog Sparepart & Oli")
        print("[0] Logout / Ganti Akun")
        print("=" * 60)

        pilihan = input("Pilih Menu (0-3): ").strip()
        if pilihan == "1":
          menu_antrean(username, role)
        elif pilihan == "2":
          os.system("cls" if os.name == "nt" else "clear")
          lihat_antrean(username, role)
          input("\nTekan Enter untuk kembali...")
        elif pilihan == "3":
          os.system("cls" if os.name == "nt" else "clear")
          lihat_inventaris()
          input("\nTekan Enter untuk kembali...")
        elif pilihan == "0":
          print("\nLogging out...")
          break
        else:
          print("❌ Pilihan tidak valid.")
          input("Tekan Enter...")


if __name__ == "__main__":
  main()
import os
from file_handler import baca_file, simpan_file

FILE_USER = "users.txt"


def inisialisasi_admin():
  """Membuat akun default admin jika file masih kosong"""
  users = baca_file(FILE_USER)
  if not users:
    # Akun default: admin | pass: admin123 | role: admin
    users.append(["admin", "admin123", "admin"])
    simpan_file(FILE_USER, users)


def register_pelanggan():
  os.system("cls" if os.name == "nt" else "clear")
  print("=" * 50)
  print("      REGISTRASI AKUN PELANGGAN - YAMAN AUTO      ")
  print("=" * 50)

  users = baca_file(FILE_USER)
  username = input("Masukkan Username Baru : ").strip()

  try:
    if not username:
      raise ValueError("Username tidak boleh kosong!")

    # Cek duplikasi username (Modul 6: Dictionary/Set logic)
    for u in users:
      if u[0] == username:
        raise ValueError("Username sudah terdaftar! Pilih username lain.")

    password = input("Masukkan Password Baru : ").strip()
    if len(password) < 4:
      raise ValueError("Password minimal 4 karakter!")

    users.append([username, password, "pelanggan"])
    simpan_file(FILE_USER, users)
    print("\n✅ Registrasi Berhasil! Silakan login.")

  except ValueError as e:
    print(f"\n❌ Error Registrasi: {e}")

  input("\nTekan Enter untuk melanjutkan...")


def login():
  inisialisasi_admin()
  while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 50)
    print("      SISTEM BENGKEL MOTOR - YAMAN AUTO           ")
    print("=" * 50)
    print("[1] Login")
    print("[2] Register Pelanggan Baru")
    print("[0] Keluar Aplikasi")
    print("-" * 50)

    pilih = input("Pilih Menu (0-2): ").strip()

    if pilih == "1":
      print("\n--- LOGIN AKUN ---")
      username = input("Username : ").strip()
      password = input("Password : ").strip()

      users = baca_file(FILE_USER)
      for u in users:
        if u[0] == username and u[1] == password:
          print(f"\n✅ Login Berhasil! Selamat Datang, {username} ({u[2]}).")
          input("Tekan Enter untuk masuk ke dashboard...")
          return (username, u[2])  # Mengembalikan Tuple (Modul 5)

      print("\n❌ Username atau Password salah!")
      input("Tekan Enter untuk mencoba lagi...")

    elif pilih == "2":
      register_pelanggan()
    elif pilih == "0":
      return None
    else:
      print("❌ Pilihan tidak valid.")
      input("Tekan Enter...")
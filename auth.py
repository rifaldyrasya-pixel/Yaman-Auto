"""
auth.py
halaman 1 & 2 flowvchart: login () dan register ().
Format user.txt: username,password,role,nama_lengkap
"""
from file_handler import FILE_USER, baca_file, simpan_file, FILE_USER
import ui

def inisialisasi_admin():
    """Jika file user kosong atau tidak ada, buat user admin default."""
    if not users:
        users.append(["admin", "admin", "admin123", "Administrator"])
        simpan_file(FILE_USER, users)

def ambil_nama(username):
    """nama lengkap dari akun. jika belum ada, pakai username."""
    for u in baca_file(FILE_USER):
        if u[0] == username:
            return u[3]  if len(u) > 3 and u[3] else username
    return username


def register_pelanggan():
    """NAma lengkap dari akun. jika belum ada, pakai username."""
    ui.bersih()
    ui.judul("Register Pelanggan", ui.UNGU)
    users = baca_file(FILE_USER)

    try:
        username = ui.tanya("Username Baru                  : ")
        if not username:
            raise ValueError("Username tidak boleh kosong!")
        if "," in username:
            raise ValueError("Username tidak boleh mengandung koma!")
        if any(u[0] == username for u in users):
            raise ValueError("Username sudah ada!")


        password = ui.tanya("Password Baru                  : ")
        if len (password) < 4:
            raise ValueError("Password minimal 4 karakter!")
        if "," in password:
            raise ValueError("Password tidak boleh mengandung koma!")

        nama = ui.bersihkan_koma(ui.tanya("Nama Lengkap         : "))
        if not nama:
            raise ValueError("Nama lengkap tidak boleh kosong!")
        

        users.append([username, password, "pelanggan", nama])
        simpan_file(FILE_USER, users)
        ui.sukses("Registrasi berhasil! Silakan login.")
    except ValueError as e:
        ui.gagal(f"Eror Registrasi: {e}")


    ui.jeda()


def login():
    """Mengemblikan (username, role) bila berhasil, None jika bila memilih keluar."""
    inisialisasai_admin()


    while true:
        ui.bersih()
        ui.banner()
        ui.judul("Menu Login")
        pilih = ui.tanya("pilih menu (0-2) : ")

        if pilih == "1":
            username = ui.tanya("Username : ")
            password = ui.tanya("Password : ")
            users = baca_file(FILE_USER)

            for u in users:
                if len(u) >= 3 and u[0] == username and u[1] == password:
                    ui.sukses(f"Login berhasil! Selamat datang, {ambil_nama(username)}.")
                    ui.jeda()
                    return (username, u[2])


            ui.gagal("Username atau Password salah!")
            ui.jeda()

        elif pilih == "2":
            register_pelanggan()

        elif pilih == "0":
            return None
        else:
            ui.gagal("Pilihan tidak valid!")
            ui.jeda()           
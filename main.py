"""
main.py  -  YAMAN AUTO
Sistem Inventaris & Antrean Servis Bengkel Motor
Jalankan dengan:  python main.py

Akun admin default : admin / admin123
"""
from auth import login, ambil_nama
from inventaris import menu_inventaris_admin, lihat_inventaris
from antrean import menu_antrean, lihat_antrean
from transaksi import menu_transaksi
import ui


def main():
    while True:
        user_session = login()

        if not user_session:
            ui.bersih()
            ui.banner()
            print(ui.warna("\n  Terima kasih telah menggunakan Sistem Yaman Auto!\n".center(ui.LEBAR), ui.HIJAU))
            break

        username, role = user_session
        nama = ambil_nama(username)

        while True:
            ui.bersih()
            ui.judul(f"Dashboard {role}", ui.UNGU)
            print(f"  User Aktif : {ui.warna(nama, ui.BOLD + ui.KUNING)} ({username})")
            print(ui.warna("─" * ui.LEBAR, ui.ABU))

            if role == "admin":
                ui.menu([(1, "Kelola Inventaris"), (2, "Kelola Antrean"),
                         (3, "Transaksi & Pembayaran"), (0, "Logout")], ui.UNGU)
                pilihan = ui.tanya("Pilih Menu (0-3) : ")

                if pilihan == "1":
                    menu_inventaris_admin()
                elif pilihan == "2":
                    menu_antrean(username, role)
                elif pilihan == "3":
                    menu_transaksi(username, role)
                elif pilihan == "0":
                    print(ui.warna("\n  Logging out...", ui.KUNING))
                    break
                else:
                    ui.gagal("Pilihan tidak valid.")
                    ui.jeda()
            else:
                ui.menu([(1, "Daftar Antrean Baru"), (2, "Lihat Antrean Saya"),
                         (3, "Lihat Katalog Sparepart"), (4, "Beli Sparepart & Pembayaran"),
                         (0, "Logout")], ui.UNGU)
                pilihan = ui.tanya("Pilih Menu (0-4) : ")

                if pilihan == "1":
                    menu_antrean(username, role)
                elif pilihan == "2":
                    ui.bersih()
                    lihat_antrean(username, role)
                    ui.jeda()
                elif pilihan == "3":
                    ui.bersih()
                    lihat_inventaris()
                    ui.jeda()
                elif pilihan == "4":
                    menu_transaksi(username, role)
                elif pilihan == "0":
                    print(ui.warna("\n  Logging out...", ui.KUNING))
                    break
                else:
                    ui.gagal("Pilihan tidak valid.")
                    ui.jeda()


if __name__ == "__main__":
    main()
"""
Entry point untuk Sistem Manajemen Perpustakaan Digital.

Module ini menyediakan interface utama untuk menjalankan aplikasi.

Versi: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "fadhilyk"
__description__ = "Sistem Manajemen Perpustakaan Digital"

from .services import LibraryService, AuthService, ReportService
from .storage.database import Database
from .utils.helper import (
    clear_screen, print_header, print_separator, pause,
    get_input, get_int_input, confirm, format_table
)


class LibraryApp:
    """Main application class untuk Library Management System."""
    
    def __init__(self) -> None:
        """Initialize application with services."""
        self.database = Database()
        self.auth_service = AuthService(self.database)
        self.library_service = LibraryService(self.database)
        self.report_service = ReportService(self.library_service)
        self.running = True
    
    def run(self) -> None:
        """Run the main application loop."""
        clear_screen()
        print_header("SISTEM MANAJEMEN PERPUSTAKAAN DIGITAL")
        print("\nSelamat datang di Sistem Manajemen Perpustakaan")
        
        while self.running:
            if not self.auth_service.is_logged_in():
                self.show_login_menu()
            else:
                self.show_main_menu()
    
    def show_login_menu(self) -> None:
        """Display login menu."""
        print_header("MENU LOGIN")
        print("1. Login")
        print("2. Daftar Staff Baru (Pengaturan Awal)")
        print("3. Keluar")
        print_separator()
        
        try:
            choice = get_input("Pilih menu")
            
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register_staff()
            elif choice == "3":
                self.running = False
                print("\nTerima kasih telah menggunakan Sistem Manajemen Perpustakaan!")
            else:
                print("\nPilihan tidak valid!")
                pause()
        except Exception as e:
            print(f"\nError: {e}")
            pause()
    
    def handle_login(self) -> None:
        """Handle staff login."""
        clear_screen()
        print_header("LOGIN STAFF")
        
        try:
            username = get_input("Username")
            password = get_input("Password")
            
            user = self.auth_service.login(username, password)
            print(f"\nLogin berhasil! Selamat datang, {user.nama}")
            pause()
            clear_screen()
        except Exception as e:
            print(f"\nLogin gagal: {e}")
            pause()
    
    def handle_register_staff(self) -> None:
        """Handle staff registration."""
        clear_screen()
        print_header("DAFTAR STAFF BARU")
        
        try:
            id = get_input("ID Staff")
            nama = get_input("Nama Lengkap")
            kontak = get_input("Kontak")
            username = get_input("Username")
            password = get_input("Password (min 8 karakter)")
            
            staff = self.auth_service.register_petugas(id, nama, kontak, username, password)
            print(f"\nStaff berhasil didaftarkan: {staff.nama}")
            pause()
        except Exception as e:
            print(f"\nPendaftaran gagal: {e}")
            pause()
    
    def show_main_menu(self) -> None:
        """Display main menu after login."""
        clear_screen()
        user = self.auth_service.get_current_user()
        print_header("MENU UTAMA")
        print(f"Login sebagai: {user.nama}")
        print_separator()
        print("1. Manajemen Buku")
        print("2. Manajemen Anggota")
        print("3. Peminjaman Buku")
        print("4. Pengembalian Buku")
        print("5. Laporan")
        print("6. Logout")
        print("7. Keluar")
        print_separator()
        
        try:
            choice = get_input("Pilih menu")
            
            if choice == "1":
                self.show_book_menu()
            elif choice == "2":
                self.show_member_menu()
            elif choice == "3":
                self.handle_borrow_book()
            elif choice == "4":
                self.handle_return_book()
            elif choice == "5":
                self.show_report_menu()
            elif choice == "6":
                self.handle_logout()
            elif choice == "7":
                self.running = False
                print("\nTerima kasih telah menggunakan Sistem Manajemen Perpustakaan!")
            else:
                print("\nPilihan tidak valid!")
                pause()
        except Exception as e:
            print(f"\nError: {e}")
            pause()
    
    def show_book_menu(self) -> None:
        """Display book management menu."""
        while True:
            clear_screen()
            print_header("MANAJEMEN BUKU")
            print("1. Tambah Buku")
            print("2. Ubah Buku")
            print("3. Hapus Buku")
            print("4. Cari Buku")
            print("5. Daftar Semua Buku")
            print("0. Kembali ke Menu Utama")
            print_separator()
            
            try:
                choice = get_input("Pilih menu")
                
                if choice == "1":
                    self.handle_add_book()
                elif choice == "2":
                    self.handle_edit_book()
                elif choice == "3":
                    self.handle_delete_book()
                elif choice == "4":
                    self.handle_search_book()
                elif choice == "5":
                    self.handle_list_books()
                elif choice == "0":
                    break
                else:
                    print("\nPilihan tidak valid!")
                    pause()
            except Exception as e:
                print(f"\nError: {e}")
                pause()
    
    def handle_add_book(self) -> None:
        """Handle adding a new book."""
        clear_screen()
        print_header("TAMBAH BUKU BARU")
        
        try:
            id = get_input("ID Buku")
            judul = get_input("Judul")
            penulis = get_input("Penulis")
            penerbit = get_input("Penerbit")
            tahun = get_int_input("Tahun Terbit")
            kategori = get_input("Kategori")
            stok = get_int_input("Stok")
            
            buku = self.library_service.tambah_buku(id, judul, penulis, penerbit, tahun, kategori, stok)
            print(f"\nBuku berhasil ditambahkan: {buku.judul}")
            pause()
        except Exception as e:
            print(f"\nGagal menambahkan buku: {e}")
            pause()
    
    def handle_edit_book(self) -> None:
        """Handle editing a book."""
        clear_screen()
        print_header("UBAH BUKU")
        
        try:
            id = get_input("ID Buku yang akan diubah")
            buku = self.library_service._find_buku_by_id(id)
            
            if not buku:
                print(f"\nBuku dengan ID '{id}' tidak ditemukan!")
                pause()
                return
            
            print(f"\nSaat ini: {buku.judul} oleh {buku.penulis}")
            print("Kosongkan untuk mempertahankan nilai lama")
            print_separator()
            
            judul = get_input("Judul Baru", buku.judul)
            penulis = get_input("Penulis Baru", buku.penulis)
            penerbit = get_input("Penerbit Baru", buku.penerbit)
            tahun = get_int_input("Tahun Baru", buku.tahun)
            kategori = get_input("Kategori Baru", buku.kategori)
            stok = get_int_input("Stok Baru", buku.stok)
            
            self.library_service.edit_buku(id, judul, penulis, penerbit, tahun, kategori, stok)
            print("\nBuku berhasil diperbarui!")
            pause()
        except Exception as e:
            print(f"\nGagal mengubah buku: {e}")
            pause()
    
    def handle_delete_book(self) -> None:
        """Handle deleting a book."""
        clear_screen()
        print_header("HAPUS BUKU")
        
        try:
            id = get_input("ID Buku yang akan dihapus")
            buku = self.library_service._find_buku_by_id(id)
            
            if not buku:
                print(f"\nBuku dengan ID '{id}' tidak ditemukan!")
                pause()
                return
            
            print(f"\nBuku: {buku.judul} oleh {buku.penulis}")
            
            if confirm("Apakah Anda yakin ingin menghapus buku ini?"):
                self.library_service.hapus_buku(id)
                print("\nBuku berhasil dihapus!")
            else:
                print("\nPenghapusan dibatalkan.")
            pause()
        except Exception as e:
            print(f"\nGagal menghapus buku: {e}")
            pause()
    
    def handle_search_book(self) -> None:
        """Handle searching books."""
        clear_screen()
        print_header("CARI BUKU")
        
        try:
            keyword = get_input("Masukkan kata kunci (judul/penulis/kategori)")
            results = self.library_service.cari_buku(keyword)
            
            if results:
                data = []
                for buku in results:
                    data.append({
                        "ID": buku.id,
                        "Judul": buku.judul,
                        "Penulis": buku.penulis,
                        "Penerbit": buku.penerbit,
                        "Tahun": buku.tahun,
                        "Kategori": buku.kategori,
                        "Stok": buku.stok
                    })
                print("\n" + format_table(data))
            else:
                print("\nTidak ada buku ditemukan!")
            pause()
        except Exception as e:
            print(f"\nPencarian gagal: {e}")
            pause()
    
    def handle_list_books(self) -> None:
        """Handle listing all books."""
        clear_screen()
        print_header("SEMUA BUKU")
        
        try:
            books = self.library_service.daftar_buku()
            
            if books:
                data = []
                for buku in books:
                    data.append({
                        "ID": buku.id,
                        "Judul": buku.judul,
                        "Penulis": buku.penulis,
                        "Kategori": buku.kategori,
                        "Stok": buku.stok,
                        "Status": "Tersedia" if buku.tersedia() else "Habis"
                    })
                print("\n" + format_table(data))
            else:
                print("\nTidak ada buku di perpustakaan!")
            pause()
        except Exception as e:
            print(f"\nGagal menampilkan daftar buku: {e}")
            pause()
    
    def show_member_menu(self) -> None:
        """Display member management menu."""
        while True:
            clear_screen()
            print_header("MANAJEMEN ANGGOTA")
            print("1. Tambah Anggota")
            print("2. Ubah Anggota")
            print("3. Hapus Anggota")
            print("4. Cari Anggota")
            print("5. Daftar Semua Anggota")
            print("0. Kembali ke Menu Utama")
            print_separator()
            
            try:
                choice = get_input("Pilih menu")
                
                if choice == "1":
                    self.handle_add_member()
                elif choice == "2":
                    self.handle_edit_member()
                elif choice == "3":
                    self.handle_delete_member()
                elif choice == "4":
                    self.handle_search_member()
                elif choice == "5":
                    self.handle_list_members()
                elif choice == "0":
                    break
                else:
                    print("\nPilihan tidak valid!")
                    pause()
            except Exception as e:
                print(f"\nError: {e}")
                pause()
    
    def handle_add_member(self) -> None:
        """Handle adding a new member."""
        clear_screen()
        print_header("TAMBAH ANGGOTA BARU")
        
        try:
            id = get_input("ID Anggota")
            nama = get_input("Nama Lengkap")
            kontak = get_input("Kontak")
            alamat = get_input("Alamat")
            
            anggota = self.library_service.tambah_anggota(id, nama, kontak, alamat)
            print(f"\nAnggota berhasil ditambahkan: {anggota.nama}")
            pause()
        except Exception as e:
            print(f"\nGagal menambahkan anggota: {e}")
            pause()
    
    def handle_edit_member(self) -> None:
        """Handle editing a member."""
        clear_screen()
        print_header("UBAH ANGGOTA")
        
        try:
            id = get_input("ID Anggota yang akan diubah")
            anggota = self.library_service._find_anggota_by_id(id)
            
            if not anggota:
                print(f"\nAnggota dengan ID '{id}' tidak ditemukan!")
                pause()
                return
            
            print(f"\nSaat ini: {anggota.nama}")
            print("Kosongkan untuk mempertahankan nilai lama")
            print_separator()
            
            nama = get_input("Nama Baru", anggota.nama)
            kontak = get_input("Kontak Baru", anggota.kontak)
            alamat = get_input("Alamat Baru", anggota.alamat)
            
            self.library_service.edit_anggota(id, nama, kontak, alamat)
            print("\nAnggota berhasil diperbarui!")
            pause()
        except Exception as e:
            print(f"\nGagal mengubah anggota: {e}")
            pause()
    
    def handle_delete_member(self) -> None:
        """Handle deleting a member."""
        clear_screen()
        print_header("HAPUS ANGGOTA")
        
        try:
            id = get_input("ID Anggota yang akan dihapus")
            anggota = self.library_service._find_anggota_by_id(id)
            
            if not anggota:
                print(f"\nAnggota dengan ID '{id}' tidak ditemukan!")
                pause()
                return
            
            print(f"\nAnggota: {anggota.nama}")
            print(f"Pinjaman Aktif: {anggota.jumlah_pinjaman()}")
            
            if confirm("Apakah Anda yakin ingin menghapus anggota ini?"):
                self.library_service.hapus_anggota(id)
                print("\nAnggota berhasil dihapus!")
            else:
                print("\nPenghapusan dibatalkan.")
            pause()
        except Exception as e:
            print(f"\nGagal menghapus anggota: {e}")
            pause()
    
    def handle_search_member(self) -> None:
        """Handle searching members."""
        clear_screen()
        print_header("CARI ANGGOTA")
        
        try:
            keyword = get_input("Masukkan kata kunci (nama/kontak)")
            results = self.library_service.cari_anggota(keyword)
            
            if results:
                data = []
                for anggota in results:
                    data.append({
                        "ID": anggota.id,
                        "Nama": anggota.nama,
                        "Kontak": anggota.kontak,
                        "Alamat": anggota.alamat,
                        "Pinjaman Aktif": anggota.jumlah_pinjaman()
                    })
                print("\n" + format_table(data))
            else:
                print("\nTidak ada anggota ditemukan!")
            pause()
        except Exception as e:
            print(f"\nPencarian gagal: {e}")
            pause()
    
    def handle_list_members(self) -> None:
        """Handle listing all members."""
        clear_screen()
        print_header("SEMUA ANGGOTA")
        
        try:
            members = self.library_service.daftar_anggota()
            
            if members:
                data = []
                for anggota in members:
                    data.append({
                        "ID": anggota.id,
                        "Nama": anggota.nama,
                        "Kontak": anggota.kontak,
                        "Alamat": anggota.alamat,
                        "Pinjaman Aktif": anggota.jumlah_pinjaman()
                    })
                print("\n" + format_table(data))
            else:
                print("\nTidak ada anggota terdaftar!")
            pause()
        except Exception as e:
            print(f"\nGagal menampilkan daftar anggota: {e}")
            pause()
    
    def handle_borrow_book(self) -> None:
        """Handle borrowing a book."""
        clear_screen()
        print_header("PEMINJAMAN BUKU")
        
        try:
            anggota_id = get_input("ID Anggota")
            buku_id = get_input("ID Buku")
            
            peminjaman = self.library_service.pinjam_buku(anggota_id, buku_id)
            
            anggota = self.library_service._find_anggota_by_id(anggota_id)
            buku = self.library_service._find_buku_by_id(buku_id)
            
            print("\n" + "=" * 50)
            print("PEMINJAMAN BERHASIL")
            print("=" * 50)
            print(f"ID Transaksi: {peminjaman.id}")
            print(f"Anggota: {anggota.nama}")
            print(f"Buku: {buku.judul}")
            print(f"Tanggal Pinjam: {peminjaman.tanggal_pinjam.strftime('%Y-%m-%d %H:%M')}")
            print(f"Jatuh Tempo: {peminjaman.jatuh_tempo.strftime('%Y-%m-%d %H:%M')}")
            print(f"Sisa Stok: {buku.stok}")
            print("=" * 50)
            pause()
        except Exception as e:
            print(f"\nPeminjaman gagal: {e}")
            pause()
    
    def handle_return_book(self) -> None:
        """Handle returning a book."""
        clear_screen()
        print_header("PENGEMBALIAN BUKU")
        
        try:
            print("Peminjaman Aktif:")
            peminjaman_aktif = self.library_service.daftar_peminjaman(status="aktif")
            
            if not peminjaman_aktif:
                print("\nTidak ada peminjaman aktif!")
                pause()
                return
            
            data = []
            for p in peminjaman_aktif:
                anggota = self.library_service._find_anggota_by_id(p.anggota_id)
                buku = self.library_service._find_buku_by_id(p.buku_id)
                data.append({
                    "ID Pinjaman": p.id[:8] + "...",
                    "Anggota": anggota.nama if anggota else "Tidak Diketahui",
                    "Buku": buku.judul if buku else "Tidak Diketahui",
                    "Jatuh Tempo": p.jatuh_tempo.strftime('%Y-%m-%d')
                })
            print("\n" + format_table(data))
            
            print_separator()
            peminjaman_id = get_input("Masukkan ID Pinjaman lengkap")
            
            peminjaman = self.library_service.kembalikan_buku(peminjaman_id)
            
            anggota = self.library_service._find_anggota_by_id(peminjaman.anggota_id)
            buku = self.library_service._find_buku_by_id(peminjaman.buku_id)
            
            print("\n" + "=" * 50)
            print("PENGEMBALIAN BERHASIL")
            print("=" * 50)
            print(f"Anggota: {anggota.nama}")
            print(f"Buku: {buku.judul}")
            print(f"Tanggal Kembali: {peminjaman.tanggal_kembali.strftime('%Y-%m-%d %H:%M')}")
            print(f"Keterlambatan: {peminjaman.terlambat()} hari")
            print(f"Denda: Rp {peminjaman.denda.nominal:,}")
            print("=" * 50)
            pause()
        except Exception as e:
            print(f"\nPengembalian gagal: {e}")
            pause()
    
    def show_report_menu(self) -> None:
        """Display report menu."""
        while True:
            clear_screen()
            print_header("LAPORAN")
            print("1. Semua Buku")
            print("2. Buku Tersedia")
            print("3. Buku Dipinjam")
            print("4. Anggota")
            print("5. Transaksi")
            print("6. Denda")
            print("7. Statistik")
            print("0. Kembali ke Menu Utama")
            print_separator()
            
            try:
                choice = get_input("Pilih menu")
                
                if choice == "1":
                    self.show_all_books_report()
                elif choice == "2":
                    self.show_available_books_report()
                elif choice == "3":
                    self.show_borrowed_books_report()
                elif choice == "4":
                    self.show_members_report()
                elif choice == "5":
                    self.show_transactions_report()
                elif choice == "6":
                    self.show_fines_report()
                elif choice == "7":
                    self.show_statistics_report()
                elif choice == "0":
                    break
                else:
                    print("\nPilihan tidak valid!")
                    pause()
            except Exception as e:
                print(f"\nError: {e}")
                pause()
    
    def show_all_books_report(self) -> None:
        """Show all books report."""
        clear_screen()
        print_header("LAPORAN: SEMUA BUKU")
        
        try:
            laporan = self.report_service.laporan_semua_buku()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nTidak ada buku di perpustakaan!")
            pause()
        except Exception as e:
            print(f"\nGagal membuat laporan: {e}")
            pause()
    
    def show_available_books_report(self) -> None:
        """Show available books report."""
        clear_screen()
        print_header("LAPORAN: BUKU TERSEDIA")
        
        try:
            laporan = self.report_service.laporan_buku_tersedia()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nTidak ada buku tersedia!")
            pause()
        except Exception as e:
            print(f"\nGagal membuat laporan: {e}")
            pause()
    
    def show_borrowed_books_report(self) -> None:
        """Show borrowed books report."""
        clear_screen()
        print_header("LAPORAN: BUKU DIPINJAM")
        
        try:
            laporan = self.report_service.laporan_buku_dipinjam()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nTidak ada buku dipinjam!")
            pause()
        except Exception as e:
            print(f"\nGagal membuat laporan: {e}")
            pause()
    
    def show_members_report(self) -> None:
        """Show members report."""
        clear_screen()
        print_header("LAPORAN: ANGGOTA")
        
        try:
            laporan = self.report_service.laporan_anggota()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nTidak ada anggota terdaftar!")
            pause()
        except Exception as e:
            print(f"\nGagal membuat laporan: {e}")
            pause()
    
    def show_transactions_report(self) -> None:
        """Show transactions report."""
        clear_screen()
        print_header("LAPORAN: TRANSAKSI")
        print("\n1. Semua Transaksi")
        print("2. Peminjaman Aktif")
        print("3. Transaksi Selesai")
        print_separator()
        
        try:
            choice = get_input("Pilih menu")
            
            if choice == "1":
                laporan = self.report_service.laporan_transaksi()
            elif choice == "2":
                laporan = self.report_service.laporan_transaksi(status="aktif")
            elif choice == "3":
                laporan = self.report_service.laporan_transaksi(status="selesai")
            else:
                print("\nPilihan tidak valid!")
                pause()
                return
            
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nTidak ada transaksi!")
            pause()
        except Exception as e:
            print(f"\nGagal membuat laporan: {e}")
            pause()
    
    def show_fines_report(self) -> None:
        """Show fines report."""
        clear_screen()
        print_header("LAPORAN: DENDA")
        
        try:
            laporan = self.report_service.laporan_denda()
            if laporan:
                print("\n" + format_table(laporan))
                total = sum(item['nominal_denda'] for item in laporan)
                print(f"\nTotal Denda: Rp {total:,}")
            else:
                print("\nTidak ada denda tercatat!")
            pause()
        except Exception as e:
            print(f"\nGagal membuat laporan: {e}")
            pause()
    
    def show_statistics_report(self) -> None:
        """Show library statistics."""
        clear_screen()
        print_header("LAPORAN: STATISTIK PERPUSTAKAAN")
        
        try:
            stats = self.report_service.statistik_perpustakaan()
            
            print("\n" + "=" * 50)
            print(f"Total Buku: {stats['total_buku']}")
            print(f"Total Stok: {stats['total_stok']}")
            print(f"Total Anggota: {stats['total_anggota']}")
            print(f"Peminjaman Aktif: {stats['total_peminjaman_aktif']}")
            print(f"Transaksi Selesai: {stats['total_peminjaman_selesai']}")
            print(f"Total Transaksi: {stats['total_peminjaman']}")
            print(f"Total Denda: Rp {stats['total_denda']:,}")
            print("=" * 50)
            pause()
        except Exception as e:
            print(f"\nGagal membuat laporan: {e}")
            pause()
    
    def handle_logout(self) -> None:
        """Handle user logout."""
        try:
            self.auth_service.logout()
            print("\nLogout berhasil!")
            pause()
            clear_screen()
        except Exception as e:
            print(f"\nLogout gagal: {e}")
            pause()


def main():
    """Main entry point."""
    app = LibraryApp()
    app.run()


if __name__ == "__main__":
    main()

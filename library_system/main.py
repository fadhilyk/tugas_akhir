"""
Entry point untuk Sistem Manajemen Perpustakaan Digital.

Module ini menyediakan interface utama untuk menjalankan aplikasi.
"""

from services import LibraryService, AuthService, ReportService
from storage.database import Database
from utils.helper import (
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
        print_header("DIGITAL LIBRARY MANAGEMENT SYSTEM")
        print("\nWelcome to the Library Management System")
        
        while self.running:
            if not self.auth_service.is_logged_in():
                self.show_login_menu()
            else:
                self.show_main_menu()
    
    def show_login_menu(self) -> None:
        """Display login menu."""
        print_header("LOGIN MENU")
        print("1. Login")
        print("2. Register New Staff (First Time Setup)")
        print("3. Exit")
        print_separator()
        
        try:
            choice = get_input("Choose option")
            
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_register_staff()
            elif choice == "3":
                self.running = False
                print("\nThank you for using Library Management System!")
            else:
                print("\nInvalid choice!")
                pause()
        except Exception as e:
            print(f"\nError: {e}")
            pause()
    
    def handle_login(self) -> None:
        """Handle staff login."""
        clear_screen()
        print_header("STAFF LOGIN")
        
        try:
            username = get_input("Username")
            password = get_input("Password")
            
            user = self.auth_service.login(username, password)
            print(f"\nLogin successful! Welcome, {user.nama}")
            pause()
            clear_screen()
        except Exception as e:
            print(f"\nLogin failed: {e}")
            pause()
    
    def handle_register_staff(self) -> None:
        """Handle staff registration."""
        clear_screen()
        print_header("REGISTER NEW STAFF")
        
        try:
            id = get_input("Staff ID")
            nama = get_input("Full Name")
            kontak = get_input("Contact")
            username = get_input("Username")
            password = get_input("Password (min 8 characters)")
            
            staff = self.auth_service.register_petugas(id, nama, kontak, username, password)
            print(f"\nStaff registered successfully: {staff.nama}")
            pause()
        except Exception as e:
            print(f"\nRegistration failed: {e}")
            pause()
    
    def show_main_menu(self) -> None:
        """Display main menu after login."""
        clear_screen()
        user = self.auth_service.get_current_user()
        print_header("MAIN MENU")
        print(f"Logged in as: {user.nama}")
        print_separator()
        print("1. Book Management")
        print("2. Member Management")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Reports")
        print("6. Logout")
        print("7. Exit")
        print_separator()
        
        try:
            choice = get_input("Choose option")
            
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
                print("\nThank you for using Library Management System!")
            else:
                print("\nInvalid choice!")
                pause()
        except Exception as e:
            print(f"\nError: {e}")
            pause()
    
    def show_book_menu(self) -> None:
        """Display book management menu."""
        while True:
            clear_screen()
            print_header("BOOK MANAGEMENT")
            print("1. Add Book")
            print("2. Edit Book")
            print("3. Delete Book")
            print("4. Search Book")
            print("5. List All Books")
            print("0. Back to Main Menu")
            print_separator()
            
            try:
                choice = get_input("Choose option")
                
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
                    print("\nInvalid choice!")
                    pause()
            except Exception as e:
                print(f"\nError: {e}")
                pause()
    
    def handle_add_book(self) -> None:
        """Handle adding a new book."""
        clear_screen()
        print_header("ADD NEW BOOK")
        
        try:
            id = get_input("Book ID")
            judul = get_input("Title")
            penulis = get_input("Author")
            penerbit = get_input("Publisher")
            tahun = get_int_input("Publication Year")
            kategori = get_input("Category")
            stok = get_int_input("Stock")
            
            buku = self.library_service.tambah_buku(id, judul, penulis, penerbit, tahun, kategori, stok)
            print(f"\nBook added successfully: {buku.judul}")
            pause()
        except Exception as e:
            print(f"\nFailed to add book: {e}")
            pause()
    
    def handle_edit_book(self) -> None:
        """Handle editing a book."""
        clear_screen()
        print_header("EDIT BOOK")
        
        try:
            id = get_input("Book ID to edit")
            buku = self.library_service._find_buku_by_id(id)
            
            if not buku:
                print(f"\nBook with ID '{id}' not found!")
                pause()
                return
            
            print(f"\nCurrent: {buku.judul} by {buku.penulis}")
            print("Leave blank to keep current value")
            print_separator()
            
            judul = get_input("New Title", buku.judul)
            penulis = get_input("New Author", buku.penulis)
            penerbit = get_input("New Publisher", buku.penerbit)
            tahun = get_int_input("New Year", buku.tahun)
            kategori = get_input("New Category", buku.kategori)
            stok = get_int_input("New Stock", buku.stok)
            
            self.library_service.edit_buku(id, judul, penulis, penerbit, tahun, kategori, stok)
            print("\nBook updated successfully!")
            pause()
        except Exception as e:
            print(f"\nFailed to edit book: {e}")
            pause()
    
    def handle_delete_book(self) -> None:
        """Handle deleting a book."""
        clear_screen()
        print_header("DELETE BOOK")
        
        try:
            id = get_input("Book ID to delete")
            buku = self.library_service._find_buku_by_id(id)
            
            if not buku:
                print(f"\nBook with ID '{id}' not found!")
                pause()
                return
            
            print(f"\nBook: {buku.judul} by {buku.penulis}")
            
            if confirm("Are you sure you want to delete this book?"):
                self.library_service.hapus_buku(id)
                print("\nBook deleted successfully!")
            else:
                print("\nDeletion cancelled.")
            pause()
        except Exception as e:
            print(f"\nFailed to delete book: {e}")
            pause()
    
    def handle_search_book(self) -> None:
        """Handle searching books."""
        clear_screen()
        print_header("SEARCH BOOK")
        
        try:
            keyword = get_input("Enter search keyword (title/author/category)")
            results = self.library_service.cari_buku(keyword)
            
            if results:
                data = []
                for buku in results:
                    data.append({
                        "ID": buku.id,
                        "Title": buku.judul,
                        "Author": buku.penulis,
                        "Publisher": buku.penerbit,
                        "Year": buku.tahun,
                        "Category": buku.kategori,
                        "Stock": buku.stok
                    })
                print("\n" + format_table(data))
            else:
                print("\nNo books found!")
            pause()
        except Exception as e:
            print(f"\nSearch failed: {e}")
            pause()
    
    def handle_list_books(self) -> None:
        """Handle listing all books."""
        clear_screen()
        print_header("ALL BOOKS")
        
        try:
            books = self.library_service.daftar_buku()
            
            if books:
                data = []
                for buku in books:
                    data.append({
                        "ID": buku.id,
                        "Title": buku.judul,
                        "Author": buku.penulis,
                        "Category": buku.kategori,
                        "Stock": buku.stok,
                        "Status": "Available" if buku.tersedia() else "Out of Stock"
                    })
                print("\n" + format_table(data))
            else:
                print("\nNo books in library!")
            pause()
        except Exception as e:
            print(f"\nFailed to list books: {e}")
            pause()
    
    def show_member_menu(self) -> None:
        """Display member management menu."""
        while True:
            clear_screen()
            print_header("MEMBER MANAGEMENT")
            print("1. Add Member")
            print("2. Edit Member")
            print("3. Delete Member")
            print("4. Search Member")
            print("5. List All Members")
            print("0. Back to Main Menu")
            print_separator()
            
            try:
                choice = get_input("Choose option")
                
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
                    print("\nInvalid choice!")
                    pause()
            except Exception as e:
                print(f"\nError: {e}")
                pause()
    
    def handle_add_member(self) -> None:
        """Handle adding a new member."""
        clear_screen()
        print_header("ADD NEW MEMBER")
        
        try:
            id = get_input("Member ID")
            nama = get_input("Full Name")
            kontak = get_input("Contact")
            alamat = get_input("Address")
            
            anggota = self.library_service.tambah_anggota(id, nama, kontak, alamat)
            print(f"\nMember added successfully: {anggota.nama}")
            pause()
        except Exception as e:
            print(f"\nFailed to add member: {e}")
            pause()
    
    def handle_edit_member(self) -> None:
        """Handle editing a member."""
        clear_screen()
        print_header("EDIT MEMBER")
        
        try:
            id = get_input("Member ID to edit")
            anggota = self.library_service._find_anggota_by_id(id)
            
            if not anggota:
                print(f"\nMember with ID '{id}' not found!")
                pause()
                return
            
            print(f"\nCurrent: {anggota.nama}")
            print("Leave blank to keep current value")
            print_separator()
            
            nama = get_input("New Name", anggota.nama)
            kontak = get_input("New Contact", anggota.kontak)
            alamat = get_input("New Address", anggota.alamat)
            
            self.library_service.edit_anggota(id, nama, kontak, alamat)
            print("\nMember updated successfully!")
            pause()
        except Exception as e:
            print(f"\nFailed to edit member: {e}")
            pause()
    
    def handle_delete_member(self) -> None:
        """Handle deleting a member."""
        clear_screen()
        print_header("DELETE MEMBER")
        
        try:
            id = get_input("Member ID to delete")
            anggota = self.library_service._find_anggota_by_id(id)
            
            if not anggota:
                print(f"\nMember with ID '{id}' not found!")
                pause()
                return
            
            print(f"\nMember: {anggota.nama}")
            print(f"Active Loans: {anggota.jumlah_pinjaman()}")
            
            if confirm("Are you sure you want to delete this member?"):
                self.library_service.hapus_anggota(id)
                print("\nMember deleted successfully!")
            else:
                print("\nDeletion cancelled.")
            pause()
        except Exception as e:
            print(f"\nFailed to delete member: {e}")
            pause()
    
    def handle_search_member(self) -> None:
        """Handle searching members."""
        clear_screen()
        print_header("SEARCH MEMBER")
        
        try:
            keyword = get_input("Enter search keyword (name/contact)")
            results = self.library_service.cari_anggota(keyword)
            
            if results:
                data = []
                for anggota in results:
                    data.append({
                        "ID": anggota.id,
                        "Name": anggota.nama,
                        "Contact": anggota.kontak,
                        "Address": anggota.alamat,
                        "Active Loans": anggota.jumlah_pinjaman()
                    })
                print("\n" + format_table(data))
            else:
                print("\nNo members found!")
            pause()
        except Exception as e:
            print(f"\nSearch failed: {e}")
            pause()
    
    def handle_list_members(self) -> None:
        """Handle listing all members."""
        clear_screen()
        print_header("ALL MEMBERS")
        
        try:
            members = self.library_service.daftar_anggota()
            
            if members:
                data = []
                for anggota in members:
                    data.append({
                        "ID": anggota.id,
                        "Name": anggota.nama,
                        "Contact": anggota.kontak,
                        "Address": anggota.alamat,
                        "Active Loans": anggota.jumlah_pinjaman()
                    })
                print("\n" + format_table(data))
            else:
                print("\nNo members registered!")
            pause()
        except Exception as e:
            print(f"\nFailed to list members: {e}")
            pause()
    
    def handle_borrow_book(self) -> None:
        """Handle borrowing a book."""
        clear_screen()
        print_header("BORROW BOOK")
        
        try:
            anggota_id = get_input("Member ID")
            buku_id = get_input("Book ID")
            
            peminjaman = self.library_service.pinjam_buku(anggota_id, buku_id)
            
            anggota = self.library_service._find_anggota_by_id(anggota_id)
            buku = self.library_service._find_buku_by_id(buku_id)
            
            print("\n" + "=" * 50)
            print("BORROW SUCCESSFUL")
            print("=" * 50)
            print(f"Transaction ID: {peminjaman.id}")
            print(f"Member: {anggota.nama}")
            print(f"Book: {buku.judul}")
            print(f"Borrow Date: {peminjaman.tanggal_pinjam.strftime('%Y-%m-%d %H:%M')}")
            print(f"Due Date: {peminjaman.jatuh_tempo.strftime('%Y-%m-%d %H:%M')}")
            print(f"Remaining Stock: {buku.stok}")
            print("=" * 50)
            pause()
        except Exception as e:
            print(f"\nBorrow failed: {e}")
            pause()
    
    def handle_return_book(self) -> None:
        """Handle returning a book."""
        clear_screen()
        print_header("RETURN BOOK")
        
        try:
            print("Active Loans:")
            peminjaman_aktif = self.library_service.daftar_peminjaman(status="aktif")
            
            if not peminjaman_aktif:
                print("\nNo active loans!")
                pause()
                return
            
            data = []
            for p in peminjaman_aktif:
                anggota = self.library_service._find_anggota_by_id(p.anggota_id)
                buku = self.library_service._find_buku_by_id(p.buku_id)
                data.append({
                    "Loan ID": p.id[:8] + "...",
                    "Member": anggota.nama if anggota else "Unknown",
                    "Book": buku.judul if buku else "Unknown",
                    "Due Date": p.jatuh_tempo.strftime('%Y-%m-%d')
                })
            print("\n" + format_table(data))
            
            print_separator()
            peminjaman_id = get_input("Enter full Loan ID")
            
            peminjaman = self.library_service.kembalikan_buku(peminjaman_id)
            
            anggota = self.library_service._find_anggota_by_id(peminjaman.anggota_id)
            buku = self.library_service._find_buku_by_id(peminjaman.buku_id)
            
            print("\n" + "=" * 50)
            print("RETURN SUCCESSFUL")
            print("=" * 50)
            print(f"Member: {anggota.nama}")
            print(f"Book: {buku.judul}")
            print(f"Return Date: {peminjaman.tanggal_kembali.strftime('%Y-%m-%d %H:%M')}")
            print(f"Late Days: {peminjaman.terlambat()}")
            print(f"Fine: Rp {peminjaman.denda.nominal:,}")
            print("=" * 50)
            pause()
        except Exception as e:
            print(f"\nReturn failed: {e}")
            pause()
    
    def show_report_menu(self) -> None:
        """Display report menu."""
        while True:
            clear_screen()
            print_header("REPORTS")
            print("1. All Books")
            print("2. Available Books")
            print("3. Borrowed Books")
            print("4. Members")
            print("5. Transactions")
            print("6. Fines")
            print("7. Statistics")
            print("0. Back to Main Menu")
            print_separator()
            
            try:
                choice = get_input("Choose option")
                
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
                    print("\nInvalid choice!")
                    pause()
            except Exception as e:
                print(f"\nError: {e}")
                pause()
    
    def show_all_books_report(self) -> None:
        """Show all books report."""
        clear_screen()
        print_header("REPORT: ALL BOOKS")
        
        try:
            laporan = self.report_service.laporan_semua_buku()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nNo books in library!")
            pause()
        except Exception as e:
            print(f"\nFailed to generate report: {e}")
            pause()
    
    def show_available_books_report(self) -> None:
        """Show available books report."""
        clear_screen()
        print_header("REPORT: AVAILABLE BOOKS")
        
        try:
            laporan = self.report_service.laporan_buku_tersedia()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nNo available books!")
            pause()
        except Exception as e:
            print(f"\nFailed to generate report: {e}")
            pause()
    
    def show_borrowed_books_report(self) -> None:
        """Show borrowed books report."""
        clear_screen()
        print_header("REPORT: BORROWED BOOKS")
        
        try:
            laporan = self.report_service.laporan_buku_dipinjam()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nNo borrowed books!")
            pause()
        except Exception as e:
            print(f"\nFailed to generate report: {e}")
            pause()
    
    def show_members_report(self) -> None:
        """Show members report."""
        clear_screen()
        print_header("REPORT: MEMBERS")
        
        try:
            laporan = self.report_service.laporan_anggota()
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nNo members registered!")
            pause()
        except Exception as e:
            print(f"\nFailed to generate report: {e}")
            pause()
    
    def show_transactions_report(self) -> None:
        """Show transactions report."""
        clear_screen()
        print_header("REPORT: TRANSACTIONS")
        print("\n1. All Transactions")
        print("2. Active Loans")
        print("3. Completed Transactions")
        print_separator()
        
        try:
            choice = get_input("Choose option")
            
            if choice == "1":
                laporan = self.report_service.laporan_transaksi()
            elif choice == "2":
                laporan = self.report_service.laporan_transaksi(status="aktif")
            elif choice == "3":
                laporan = self.report_service.laporan_transaksi(status="selesai")
            else:
                print("\nInvalid choice!")
                pause()
                return
            
            if laporan:
                print("\n" + format_table(laporan))
            else:
                print("\nNo transactions!")
            pause()
        except Exception as e:
            print(f"\nFailed to generate report: {e}")
            pause()
    
    def show_fines_report(self) -> None:
        """Show fines report."""
        clear_screen()
        print_header("REPORT: FINES")
        
        try:
            laporan = self.report_service.laporan_denda()
            if laporan:
                print("\n" + format_table(laporan))
                total = sum(item['nominal_denda'] for item in laporan)
                print(f"\nTotal Fines: Rp {total:,}")
            else:
                print("\nNo fines recorded!")
            pause()
        except Exception as e:
            print(f"\nFailed to generate report: {e}")
            pause()
    
    def show_statistics_report(self) -> None:
        """Show library statistics."""
        clear_screen()
        print_header("REPORT: LIBRARY STATISTICS")
        
        try:
            stats = self.report_service.statistik_perpustakaan()
            
            print("\n" + "=" * 50)
            print(f"Total Books: {stats['total_buku']}")
            print(f"Total Stock: {stats['total_stok']}")
            print(f"Total Members: {stats['total_anggota']}")
            print(f"Active Loans: {stats['total_peminjaman_aktif']}")
            print(f"Completed Transactions: {stats['total_peminjaman_selesai']}")
            print(f"Total Transactions: {stats['total_peminjaman']}")
            print(f"Total Fines: Rp {stats['total_denda']:,}")
            print("=" * 50)
            pause()
        except Exception as e:
            print(f"\nFailed to generate report: {e}")
            pause()
    
    def handle_logout(self) -> None:
        """Handle user logout."""
        try:
            self.auth_service.logout()
            print("\nLogged out successfully!")
            pause()
            clear_screen()
        except Exception as e:
            print(f"\nLogout failed: {e}")
            pause()


def main():
    """Main entry point."""
    app = LibraryApp()
    app.run()


if __name__ == "__main__":
    main()

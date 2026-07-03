"""
Tests for Loan Management.
"""

import pytest
from datetime import datetime, timedelta
from library_system.exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    LoanNotFoundError,
    BookUnavailableError,
    MaximumLoanReachedError,
    InvalidInputError
)
from library_system.models import MAX_PINJAMAN


class TestLoanBorrow:
    """Tests for borrowing books."""
    
    def test_borrow_book_success(self, library_service, sample_book, sample_member):
        """Test successfully borrowing a book."""
        loan = library_service.pinjam_buku("A001", "B001")
        
        assert loan.anggota_id == "A001"
        assert loan.buku_id == "B001"
        assert loan.status == "aktif"
        
        # Check stock reduced
        book = library_service._find_buku_by_id("B001")
        assert book.stok == 4  # Was 5, now 4
        
        # Check member loan count
        member = library_service._find_anggota_by_id("A001")
        assert member.jumlah_pinjaman() == 1
    
    def test_borrow_book_member_not_found(self, library_service, sample_book):
        """Test borrowing with non-existent member."""
        with pytest.raises(MemberNotFoundError, match="Anggota dengan ID .* tidak ditemukan"):
            library_service.pinjam_buku("A999", "B001")
    
    def test_borrow_book_not_found(self, library_service, sample_member):
        """Test borrowing non-existent book."""
        with pytest.raises(BookNotFoundError, match="Buku dengan ID .* tidak ditemukan"):
            library_service.pinjam_buku("A001", "B999")
    
    def test_borrow_book_out_of_stock(self, library_service, sample_member):
        """Test borrowing book with zero stock."""
        book = library_service.tambah_buku("B002", "Book", "Author", "Pub", 2023, "Cat", 0)
        
        with pytest.raises(BookUnavailableError, match="tidak tersedia"):
            library_service.pinjam_buku("A001", "B002")
    
    def test_borrow_book_maximum_loan_reached(self, library_service, sample_member):
        """Test borrowing when member has reached maximum loans."""
        # Add 5 books and borrow all
        for i in range(1, 6):
            library_service.tambah_buku(f"B00{i}", f"Book {i}", "Author", "Pub", 2023, "Cat", 5)
            library_service.pinjam_buku("A001", f"B00{i}")
        
        # Try to borrow 6th book
        library_service.tambah_buku("B006", "Book 6", "Author", "Pub", 2023, "Cat", 5)
        
        with pytest.raises(MaximumLoanReachedError, match=f"batas maksimal peminjaman \\({MAX_PINJAMAN} buku\\)"):
            library_service.pinjam_buku("A001", "B006")
    
    def test_borrow_book_due_date(self, library_service, sample_book, sample_member):
        """Test loan has correct due date (7 days)."""
        loan = library_service.pinjam_buku("A001", "B001")
        
        expected_due = loan.tanggal_pinjam + timedelta(days=7)
        assert loan.jatuh_tempo.date() == expected_due.date()


class TestLoanReturn:
    """Tests for returning books."""
    
    def test_return_book_success(self, library_service, sample_loan):
        """Test successfully returning a book."""
        returned = library_service.kembalikan_buku(sample_loan.id)
        
        assert returned.status == "selesai"
        assert returned.tanggal_kembali is not None
        
        # Check stock increased
        book = library_service._find_buku_by_id("B001")
        assert book.stok == 5  # Back to original
        
        # Check member loan count
        member = library_service._find_anggota_by_id("A001")
        assert member.jumlah_pinjaman() == 0
    
    def test_return_book_not_found(self, library_service):
        """Test returning non-existent loan."""
        with pytest.raises(LoanNotFoundError, match="Peminjaman dengan ID .* tidak ditemukan"):
            library_service.kembalikan_buku("invalid-loan-id")
    
    def test_return_book_already_returned(self, library_service, sample_loan):
        """Test returning already returned book."""
        library_service.kembalikan_buku(sample_loan.id)
        
        with pytest.raises(InvalidInputError, match="Peminjaman sudah selesai"):
            library_service.kembalikan_buku(sample_loan.id)


class TestLoanFineCalculation:
    """Tests for fine calculation."""
    
    def test_fine_on_time_return(self, library_service, sample_loan):
        """Test no fine for on-time return."""
        returned = library_service.kembalikan_buku(sample_loan.id)
        
        assert returned.terlambat() == 0
        assert returned.denda.nominal == 0
    
    def test_fine_late_return(self, library_service, sample_book, sample_member):
        """Test fine calculation for late return."""
        # Create loan with past due date
        loan = library_service.pinjam_buku("A001", "B001")
        
        # Manually set dates to simulate late return
        loan.tanggal_pinjam = datetime.now() - timedelta(days=10)
        loan.jatuh_tempo = datetime.now() - timedelta(days=3)
        
        # Return book
        loan.tandai_dikembalikan()
        
        assert loan.terlambat() == 3
        assert loan.denda.nominal == 6000  # 3 days * Rp 2000
    
    def test_fine_calculation_formula(self, library_service):
        """Test fine calculation formula (Rp 2000/day)."""
        from library_system.models import DENDA_PER_HARI
        
        book = library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        member = library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        
        loan = library_service.pinjam_buku("A001", "B001")
        
        # Simulate 5 days late
        loan.tanggal_pinjam = datetime.now() - timedelta(days=12)
        loan.jatuh_tempo = datetime.now() - timedelta(days=5)
        loan.tandai_dikembalikan()
        
        expected_fine = 5 * DENDA_PER_HARI
        assert loan.denda.nominal == expected_fine


class TestLoanList:
    """Tests for listing loans."""
    
    def test_list_all_loans(self, library_service, sample_loan):
        """Test listing all loans."""
        loans = library_service.daftar_peminjaman()
        
        assert len(loans) == 1
    
    def test_list_active_loans(self, library_service, sample_loan):
        """Test listing only active loans."""
        loans = library_service.daftar_peminjaman(status="aktif")
        
        assert len(loans) == 1
        assert loans[0].status == "aktif"
    
    def test_list_completed_loans(self, library_service, sample_loan):
        """Test listing completed loans."""
        library_service.kembalikan_buku(sample_loan.id)
        
        loans = library_service.daftar_peminjaman(status="selesai")
        
        assert len(loans) == 1
        assert loans[0].status == "selesai"
    
    def test_list_loans_by_member(self, library_service):
        """Test listing loans by specific member."""
        # Create 2 members and loans
        library_service.tambah_anggota("A001", "Member 1", "081111111111", "Addr1")
        library_service.tambah_anggota("A002", "Member 2", "082222222222", "Addr2")
        library_service.tambah_buku("B001", "Book 1", "Author", "Pub", 2023, "Cat", 5)
        library_service.tambah_buku("B002", "Book 2", "Author", "Pub", 2023, "Cat", 5)
        
        library_service.pinjam_buku("A001", "B001")
        library_service.pinjam_buku("A002", "B002")
        
        loans = library_service.get_peminjaman_by_anggota("A001")
        
        assert len(loans) == 1
        assert loans[0].anggota_id == "A001"
    
    def test_list_loans_by_book(self, library_service):
        """Test listing loans for specific book."""
        library_service.tambah_anggota("A001", "Member 1", "081111111111", "Addr1")
        library_service.tambah_anggota("A002", "Member 2", "082222222222", "Addr2")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        loan1 = library_service.pinjam_buku("A001", "B001")
        library_service.kembalikan_buku(loan1.id)
        library_service.pinjam_buku("A002", "B001")
        
        loans = library_service.get_peminjaman_by_buku("B001")
        
        assert len(loans) == 2


class TestLoanStockManagement:
    """Tests for stock management during loans."""
    
    def test_stock_reduced_on_borrow(self, library_service, sample_book, sample_member):
        """Test stock is reduced when book is borrowed."""
        initial_stock = sample_book.stok
        
        library_service.pinjam_buku("A001", "B001")
        
        book = library_service._find_buku_by_id("B001")
        assert book.stok == initial_stock - 1
    
    def test_stock_restored_on_return(self, library_service, sample_loan):
        """Test stock is restored when book is returned."""
        book_before = library_service._find_buku_by_id("B001")
        stock_before = book_before.stok
        
        library_service.kembalikan_buku(sample_loan.id)
        
        book_after = library_service._find_buku_by_id("B001")
        assert book_after.stok == stock_before + 1

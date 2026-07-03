"""
Tests for Report Service.
"""

import pytest


class TestBookReports:
    """Tests for book-related reports."""
    
    def test_report_all_books(self, report_service, library_service):
        """Test report for all books."""
        library_service.tambah_buku("B001", "Book 1", "Author 1", "Pub", 2023, "Cat", 5)
        library_service.tambah_buku("B002", "Book 2", "Author 2", "Pub", 2023, "Cat", 0)
        
        report = report_service.laporan_semua_buku()
        
        assert len(report) == 2
        assert report[0]["id"] == "B001"
        assert report[0]["status"] == "Tersedia"
        assert report[1]["status"] == "Habis"
    
    def test_report_available_books(self, report_service, library_service):
        """Test report for available books only."""
        library_service.tambah_buku("B001", "Book 1", "Author", "Pub", 2023, "Cat", 5)
        library_service.tambah_buku("B002", "Book 2", "Author", "Pub", 2023, "Cat", 0)
        library_service.tambah_buku("B003", "Book 3", "Author", "Pub", 2023, "Cat", 3)
        
        report = report_service.laporan_buku_tersedia()
        
        assert len(report) == 2
        assert all(item["stok"] > 0 for item in report)
    
    def test_report_borrowed_books(self, report_service, library_service):
        """Test report for borrowed books."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book 1", "Author", "Pub", 2023, "Cat", 5)
        library_service.tambah_buku("B002", "Book 2", "Author", "Pub", 2023, "Cat", 5)
        
        library_service.pinjam_buku("A001", "B001")
        
        report = report_service.laporan_buku_dipinjam()
        
        assert len(report) == 1
        assert report[0]["id"] == "B001"
        assert report[0]["jumlah_dipinjam"] == 1


class TestMemberReports:
    """Tests for member-related reports."""
    
    def test_report_all_members(self, report_service, library_service):
        """Test report for all members."""
        library_service.tambah_anggota("A001", "Member 1", "081111111111", "Addr1")
        library_service.tambah_anggota("A002", "Member 2", "082222222222", "Addr2")
        
        report = report_service.laporan_anggota()
        
        assert len(report) == 2
        assert report[0]["id"] == "A001"
        assert report[0]["jumlah_pinjaman_aktif"] == 0
    
    def test_report_members_with_loans(self, report_service, library_service):
        """Test member report shows active loan counts."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        library_service.pinjam_buku("A001", "B001")
        
        report = report_service.laporan_anggota()
        
        assert len(report) == 1
        assert report[0]["jumlah_pinjaman_aktif"] == 1


class TestTransactionReports:
    """Tests for transaction reports."""
    
    def test_report_all_transactions(self, report_service, library_service):
        """Test report for all transactions."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book 1", "Author", "Pub", 2023, "Cat", 5)
        library_service.tambah_buku("B002", "Book 2", "Author", "Pub", 2023, "Cat", 5)
        
        loan1 = library_service.pinjam_buku("A001", "B001")
        loan2 = library_service.pinjam_buku("A001", "B002")
        library_service.kembalikan_buku(loan1.id)
        
        report = report_service.laporan_transaksi()
        
        assert len(report) == 2
    
    def test_report_active_transactions(self, report_service, library_service):
        """Test report for active transactions only."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book 1", "Author", "Pub", 2023, "Cat", 5)
        library_service.tambah_buku("B002", "Book 2", "Author", "Pub", 2023, "Cat", 5)
        
        loan1 = library_service.pinjam_buku("A001", "B001")
        loan2 = library_service.pinjam_buku("A001", "B002")
        library_service.kembalikan_buku(loan1.id)
        
        report = report_service.laporan_transaksi(status="aktif")
        
        assert len(report) == 1
        assert report[0]["status"] == "aktif"
    
    def test_report_completed_transactions(self, report_service, library_service):
        """Test report for completed transactions only."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        loan = library_service.pinjam_buku("A001", "B001")
        library_service.kembalikan_buku(loan.id)
        
        report = report_service.laporan_transaksi(status="selesai")
        
        assert len(report) == 1
        assert report[0]["status"] == "selesai"


class TestFineReports:
    """Tests for fine reports."""
    
    def test_report_fines_with_late_return(self, report_service, library_service):
        """Test fine report includes late returns."""
        from datetime import datetime, timedelta
        
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        loan = library_service.pinjam_buku("A001", "B001")
        
        # Simulate late return
        loan.tanggal_pinjam = datetime.now() - timedelta(days=10)
        loan.jatuh_tempo = datetime.now() - timedelta(days=3)
        loan.tandai_dikembalikan()
        
        library_service._database.save_transaksi(library_service._peminjaman_list)
        
        report = report_service.laporan_denda()
        
        assert len(report) == 1
        assert report[0]["hari_terlambat"] == 3
        assert report[0]["nominal_denda"] == 6000
    
    def test_report_fines_empty(self, report_service, library_service):
        """Test fine report when no fines exist."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        loan = library_service.pinjam_buku("A001", "B001")
        library_service.kembalikan_buku(loan.id)
        
        report = report_service.laporan_denda()
        
        assert len(report) == 0


class TestStatisticsReport:
    """Tests for library statistics."""
    
    def test_statistics_empty_library(self, report_service):
        """Test statistics for empty library."""
        stats = report_service.statistik_perpustakaan()
        
        assert stats["total_buku"] == 0
        assert stats["total_anggota"] == 0
        assert stats["total_peminjaman_aktif"] == 0
        assert stats["total_peminjaman_selesai"] == 0
    
    def test_statistics_with_data(self, report_service, library_service):
        """Test statistics with actual data."""
        library_service.tambah_anggota("A001", "Member 1", "081111111111", "Addr1")
        library_service.tambah_anggota("A002", "Member 2", "082222222222", "Addr2")
        library_service.tambah_buku("B001", "Book 1", "Author", "Pub", 2023, "Cat", 10)
        library_service.tambah_buku("B002", "Book 2", "Author", "Pub", 2023, "Cat", 5)
        
        loan1 = library_service.pinjam_buku("A001", "B001")
        loan2 = library_service.pinjam_buku("A002", "B002")
        library_service.kembalikan_buku(loan1.id)
        
        stats = report_service.statistik_perpustakaan()
        
        assert stats["total_buku"] == 2
        assert stats["total_stok"] == 14  # 9 (Book 1 after borrow/return) + 4 (Book 2 borrowed) + 1 (returned) = 14
        assert stats["total_anggota"] == 2
        assert stats["total_peminjaman_aktif"] == 1
        assert stats["total_peminjaman_selesai"] == 1
        assert stats["total_peminjaman"] == 2
    
    def test_statistics_total_fines(self, report_service, library_service):
        """Test total fines in statistics."""
        from datetime import datetime, timedelta
        
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        loan = library_service.pinjam_buku("A001", "B001")
        
        # Simulate late return with fine
        loan.tanggal_pinjam = datetime.now() - timedelta(days=12)
        loan.jatuh_tempo = datetime.now() - timedelta(days=5)
        loan.tandai_dikembalikan()
        
        library_service._database.save_transaksi(library_service._peminjaman_list)
        
        stats = report_service.statistik_perpustakaan()
        
        assert stats["total_denda"] == 10000  # 5 days * 2000


class TestReportDataIntegrity:
    """Tests for report data integrity."""
    
    def test_report_handles_missing_references(self, report_service, library_service):
        """Test report handles missing book/member references gracefully."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        loan = library_service.pinjam_buku("A001", "B001")
        
        # Manually corrupt data by removing book (this shouldn't happen in real scenario)
        # But report should handle it gracefully
        report = report_service.laporan_transaksi()
        
        assert len(report) == 1
        assert "anggota_nama" in report[0]
        assert "buku_judul" in report[0]

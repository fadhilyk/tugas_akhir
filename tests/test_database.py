"""
Tests for Database (JSON Storage).
"""

import pytest
import json
from pathlib import Path
from library_system.exceptions import DatabaseError


class TestDatabaseInitialization:
    """Tests for database initialization."""
    
    def test_database_creates_directory(self, temp_data_dir):
        """Test database creates data directory if not exists."""
        from library_system.storage.database import Database
        
        db = Database(data_dir=temp_data_dir)
        
        assert Path(temp_data_dir).exists()
    
    def test_database_creates_json_files(self, temp_data_dir):
        """Test database creates JSON files if not exist."""
        from library_system.storage.database import Database
        
        db = Database(data_dir=temp_data_dir)
        
        assert db.buku_file.exists()
        assert db.anggota_file.exists()
        assert db.petugas_file.exists()
        assert db.transaksi_file.exists()


class TestDatabaseSaveLoad:
    """Tests for saving and loading data."""
    
    def test_save_and_load_books(self, database, library_service):
        """Test saving and loading books."""
        library_service.tambah_buku("B001", "Test Book", "Author", "Pub", 2023, "Cat", 5)
        
        # Create new service instance to force reload
        from library_system.services import LibraryService
        new_service = LibraryService(database)
        
        books = new_service.daftar_buku()
        assert len(books) == 1
        assert books[0].judul == "Test Book"
    
    def test_save_and_load_members(self, database, library_service):
        """Test saving and loading members."""
        library_service.tambah_anggota("A001", "Test Member", "081234567890", "Address")
        
        from library_system.services import LibraryService
        new_service = LibraryService(database)
        
        members = new_service.daftar_anggota()
        assert len(members) == 1
        assert members[0].nama == "Test Member"
    
    def test_save_and_load_staff(self, database, auth_service):
        """Test saving and loading staff."""
        auth_service.register_petugas("P001", "Admin", "081234567890", "admin", "password123")
        
        from library_system.services import AuthService
        new_service = AuthService(database)
        
        staff_list = new_service.get_all_petugas()
        assert len(staff_list) == 1
        assert staff_list[0].username == "admin"
    
    def test_save_and_load_transactions(self, database, library_service):
        """Test saving and loading transactions."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        library_service.pinjam_buku("A001", "B001")
        
        from library_system.services import LibraryService
        new_service = LibraryService(database)
        
        loans = new_service.daftar_peminjaman()
        assert len(loans) == 1


class TestDatabaseSerialization:
    """Tests for data serialization."""
    
    def test_serialize_book(self, database):
        """Test book serialization."""
        from library_system.models import Buku
        
        book = Buku("B001", "Title", "Author", "Pub", 2023, "Cat", 5)
        serialized = database._serialize_buku(book)
        
        assert serialized["id"] == "B001"
        assert serialized["judul"] == "Title"
        assert serialized["stok"] == 5
    
    def test_deserialize_book(self, database):
        """Test book deserialization."""
        data = {
            "id": "B001",
            "judul": "Title",
            "penulis": "Author",
            "penerbit": "Pub",
            "tahun": 2023,
            "kategori": "Cat",
            "stok": 5
        }
        
        book = database._deserialize_buku(data)
        
        assert book.id == "B001"
        assert book.judul == "Title"
    
    def test_serialize_loan_with_datetime(self, database, library_service):
        """Test loan serialization includes datetime in ISO format."""
        library_service.tambah_anggota("A001", "Member", "081234567890", "Address")
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        loan = library_service.pinjam_buku("A001", "B001")
        
        serialized = database._serialize_peminjaman(loan)
        
        assert "tanggal_pinjam" in serialized
        assert "T" in serialized["tanggal_pinjam"]  # ISO format
        assert "jatuh_tempo" in serialized
    
    def test_deserialize_loan_with_datetime(self, database):
        """Test loan deserialization parses datetime correctly."""
        from datetime import datetime
        
        data = {
            "id": "loan-1",
            "anggota_id": "A001",
            "buku_id": "B001",
            "tanggal_pinjam": "2026-07-03T10:00:00",
            "jatuh_tempo": "2026-07-10T10:00:00",
            "tanggal_kembali": None,
            "status": "aktif",
            "denda": {"nominal": 0, "status_pembayaran": False}
        }
        
        loan = database._deserialize_peminjaman(data)
        
        assert isinstance(loan.tanggal_pinjam, datetime)
        assert loan.tanggal_kembali is None


class TestDatabaseErrorHandling:
    """Tests for database error handling."""
    
    def test_load_corrupted_json(self, database, temp_data_dir):
        """Test loading corrupted JSON file."""
        # Write invalid JSON
        corrupted_file = Path(temp_data_dir) / "buku.json"
        with open(corrupted_file, 'w') as f:
            f.write("{invalid json")
        
        # Should return empty list instead of crashing
        books = database.load_buku()
        assert books == []
    
    def test_load_empty_json_file(self, database, temp_data_dir):
        """Test loading empty JSON file."""
        empty_file = Path(temp_data_dir) / "anggota.json"
        with open(empty_file, 'w') as f:
            f.write("")
        
        members = database.load_anggota()
        assert members == []
    
    def test_load_non_array_json(self, database, temp_data_dir):
        """Test loading JSON that's not an array."""
        invalid_file = Path(temp_data_dir) / "petugas.json"
        with open(invalid_file, 'w') as f:
            json.dump({"key": "value"}, f)
        
        # Should handle gracefully
        staff = database.load_petugas()
        assert staff == []


class TestDatabaseBackup:
    """Tests for database backup functionality."""
    
    def test_backup_creates_files(self, database, library_service, temp_data_dir):
        """Test backup creates backup files."""
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        database.backup(backup_suffix="test")
        
        backup_dir = Path(temp_data_dir) / "backups"
        assert backup_dir.exists()
        
        backup_file = backup_dir / "buku_test.json"
        assert backup_file.exists()
    
    def test_backup_with_timestamp(self, database, library_service):
        """Test backup with automatic timestamp."""
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        database.backup()  # Uses timestamp
        
        # Check that backup directory was created
        backup_dir = database.data_dir / "backups"
        assert backup_dir.exists()


class TestDatabasePersistence:
    """Tests for data persistence across instances."""
    
    def test_data_persists_across_instances(self, temp_data_dir):
        """Test data persists when creating new database instance."""
        from library_system.storage.database import Database
        from library_system.services import LibraryService
        
        # First instance
        db1 = Database(data_dir=temp_data_dir)
        service1 = LibraryService(db1)
        service1.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        # Second instance (simulates app restart)
        db2 = Database(data_dir=temp_data_dir)
        service2 = LibraryService(db2)
        
        books = service2.daftar_buku()
        assert len(books) == 1
        assert books[0].id == "B001"
    
    def test_loan_data_persists_with_relationships(self, temp_data_dir):
        """Test loan data with relationships persists correctly."""
        from library_system.storage.database import Database
        from library_system.services import LibraryService
        
        # Create loan
        db1 = Database(data_dir=temp_data_dir)
        service1 = LibraryService(db1)
        service1.tambah_anggota("A001", "Member", "081234567890", "Address")
        service1.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        service1.pinjam_buku("A001", "B001")
        
        # Load in new instance
        db2 = Database(data_dir=temp_data_dir)
        service2 = LibraryService(db2)
        
        loans = service2.daftar_peminjaman()
        assert len(loans) == 1
        assert loans[0].anggota_id == "A001"
        assert loans[0].buku_id == "B001"
        
        # Verify stock was persisted
        book = service2._find_buku_by_id("B001")
        assert book.stok == 4


class TestDatabaseJSONFormat:
    """Tests for JSON file format."""
    
    def test_json_file_is_valid_json(self, database, library_service, temp_data_dir):
        """Test saved JSON files are valid JSON."""
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        json_file = Path(temp_data_dir) / "buku.json"
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Should not raise exception
        
        assert isinstance(data, list)
        assert len(data) == 1
    
    def test_json_file_uses_utf8_encoding(self, database, library_service, temp_data_dir):
        """Test JSON files use UTF-8 encoding for special characters."""
        library_service.tambah_buku("B001", "Buku Bahasa Indonesia", "Penulis", "Penerbit", 2023, "Kategori", 5)
        
        json_file = Path(temp_data_dir) / "buku.json"
        
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Buku Bahasa Indonesia" in content

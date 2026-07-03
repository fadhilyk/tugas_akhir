"""
Pytest configuration and fixtures.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from library_system.storage.database import Database
from library_system.services import LibraryService, AuthService, ReportService


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def database(temp_data_dir):
    """Create a Database instance with temporary directory."""
    return Database(data_dir=temp_data_dir)


@pytest.fixture
def auth_service(database):
    """Create an AuthService instance with test database."""
    return AuthService(database)


@pytest.fixture
def library_service(database):
    """Create a LibraryService instance with test database."""
    return LibraryService(database)


@pytest.fixture
def report_service(library_service):
    """Create a ReportService instance with test library service."""
    return ReportService(library_service)


@pytest.fixture
def sample_staff(auth_service):
    """Register a sample staff member."""
    return auth_service.register_petugas(
        id="P001",
        nama="Test Admin",
        kontak="081234567890",
        username="testadmin",
        password="password123"
    )


@pytest.fixture
def sample_book(library_service):
    """Add a sample book."""
    return library_service.tambah_buku(
        id="B001",
        judul="Test Book",
        penulis="Test Author",
        penerbit="Test Publisher",
        tahun=2023,
        kategori="Test Category",
        stok=5
    )


@pytest.fixture
def sample_member(library_service):
    """Add a sample member."""
    return library_service.tambah_anggota(
        id="A001",
        nama="Test Member",
        kontak="081234567891",
        alamat="Test Address"
    )


@pytest.fixture
def sample_loan(library_service, sample_book, sample_member):
    """Create a sample loan."""
    return library_service.pinjam_buku("A001", "B001")

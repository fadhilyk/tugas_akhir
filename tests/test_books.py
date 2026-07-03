"""
Tests for Book Management.
"""

import pytest
from library_system.exceptions import (
    BookNotFoundError,
    DuplicateIDError,
    InvalidInputError
)


class TestBookAdd:
    """Tests for adding books."""
    
    def test_add_book_success(self, library_service):
        """Test successfully adding a book."""
        book = library_service.tambah_buku(
            id="B001",
            judul="Python Programming",
            penulis="John Doe",
            penerbit="Tech Publisher",
            tahun=2023,
            kategori="Programming",
            stok=10
        )
        
        assert book.id == "B001"
        assert book.judul == "Python Programming"
        assert book.penulis == "John Doe"
        assert book.stok == 10
    
    def test_add_book_duplicate_id(self, library_service, sample_book):
        """Test adding a book with duplicate ID."""
        with pytest.raises(DuplicateIDError, match="Buku dengan ID .* sudah ada"):
            library_service.tambah_buku(
                id="B001",
                judul="Another Book",
                penulis="Jane Doe",
                penerbit="Publisher",
                tahun=2024,
                kategori="Fiction",
                stok=5
            )
    
    def test_add_book_empty_title(self, library_service):
        """Test adding a book with empty title."""
        with pytest.raises(ValueError, match="Judul tidak boleh kosong"):
            library_service.tambah_buku(
                id="B001",
                judul="",
                penulis="John Doe",
                penerbit="Publisher",
                tahun=2023,
                kategori="Fiction",
                stok=5
            )
    
    def test_add_book_negative_stock(self, library_service):
        """Test adding a book with negative stock."""
        with pytest.raises(ValueError, match="Stok tidak boleh negatif"):
            library_service.tambah_buku(
                id="B001",
                judul="Test Book",
                penulis="John Doe",
                penerbit="Publisher",
                tahun=2023,
                kategori="Fiction",
                stok=-5
            )


class TestBookEdit:
    """Tests for editing books."""
    
    def test_edit_book_title(self, library_service, sample_book):
        """Test editing book title."""
        updated = library_service.edit_buku("B001", judul="Updated Title")
        
        assert updated.judul == "Updated Title"
        assert updated.penulis == "Test Author"  # Unchanged
    
    def test_edit_book_multiple_fields(self, library_service, sample_book):
        """Test editing multiple book fields."""
        updated = library_service.edit_buku(
            "B001",
            judul="New Title",
            penulis="New Author",
            stok=10
        )
        
        assert updated.judul == "New Title"
        assert updated.penulis == "New Author"
        assert updated.stok == 10
    
    def test_edit_book_not_found(self, library_service):
        """Test editing non-existent book."""
        with pytest.raises(BookNotFoundError, match="Buku dengan ID .* tidak ditemukan"):
            library_service.edit_buku("B999", judul="Title")
    
    def test_edit_book_empty_title(self, library_service, sample_book):
        """Test editing book with empty title."""
        with pytest.raises(InvalidInputError, match="Judul tidak boleh kosong"):
            library_service.edit_buku("B001", judul="")
    
    def test_edit_book_negative_stock(self, library_service, sample_book):
        """Test editing book with negative stock."""
        with pytest.raises(InvalidInputError, match="Stok tidak boleh negatif"):
            library_service.edit_buku("B001", stok=-1)


class TestBookDelete:
    """Tests for deleting books."""
    
    def test_delete_book_success(self, library_service, sample_book):
        """Test successfully deleting a book."""
        library_service.hapus_buku("B001")
        
        books = library_service.daftar_buku()
        assert len(books) == 0
    
    def test_delete_book_not_found(self, library_service):
        """Test deleting non-existent book."""
        with pytest.raises(BookNotFoundError, match="Buku dengan ID .* tidak ditemukan"):
            library_service.hapus_buku("B999")
    
    def test_delete_book_with_active_loan(self, library_service, sample_loan):
        """Test deleting a book that is currently borrowed."""
        with pytest.raises(InvalidInputError, match="Buku masih dipinjam"):
            library_service.hapus_buku("B001")


class TestBookSearch:
    """Tests for searching books."""
    
    def test_search_book_by_title(self, library_service):
        """Test searching books by title."""
        library_service.tambah_buku("B001", "Python Programming", "Author", "Pub", 2023, "Tech", 5)
        library_service.tambah_buku("B002", "Java Programming", "Author", "Pub", 2023, "Tech", 5)
        
        results = library_service.cari_buku("Python")
        
        assert len(results) == 1
        assert results[0].judul == "Python Programming"
    
    def test_search_book_by_author(self, library_service):
        """Test searching books by author."""
        library_service.tambah_buku("B001", "Book A", "John Doe", "Pub", 2023, "Fiction", 5)
        library_service.tambah_buku("B002", "Book B", "Jane Smith", "Pub", 2023, "Fiction", 5)
        
        results = library_service.cari_buku("John")
        
        assert len(results) == 1
        assert results[0].penulis == "John Doe"
    
    def test_search_book_case_insensitive(self, library_service, sample_book):
        """Test case-insensitive search."""
        results = library_service.cari_buku("test")
        
        assert len(results) == 1
        assert results[0].judul == "Test Book"
    
    def test_search_book_no_results(self, library_service, sample_book):
        """Test search with no matching results."""
        results = library_service.cari_buku("NonExistent")
        
        assert len(results) == 0


class TestBookList:
    """Tests for listing books."""
    
    def test_list_all_books(self, library_service):
        """Test listing all books."""
        library_service.tambah_buku("B001", "Book 1", "Author", "Pub", 2023, "Cat", 5)
        library_service.tambah_buku("B002", "Book 2", "Author", "Pub", 2023, "Cat", 3)
        
        books = library_service.daftar_buku()
        
        assert len(books) == 2
    
    def test_list_books_empty(self, library_service):
        """Test listing books when none exist."""
        books = library_service.daftar_buku()
        
        assert len(books) == 0


class TestBookAvailability:
    """Tests for book availability."""
    
    def test_book_available(self, library_service, sample_book):
        """Test checking if book is available."""
        book = library_service._find_buku_by_id("B001")
        
        assert book.tersedia()
    
    def test_book_unavailable(self, library_service):
        """Test book with zero stock is unavailable."""
        book = library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 0)
        
        assert not book.tersedia()

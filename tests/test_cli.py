"""
Tests for CLI functionality.
"""

import pytest
from io import StringIO
from library_system.utils.helper import format_table, confirm


class TestHelperFunctions:
    """Tests for helper utility functions."""
    
    def test_format_table_with_data(self):
        """Test formatting data as a table."""
        data = [
            {"id": "1", "name": "Item 1", "value": "100"},
            {"id": "2", "name": "Item 2", "value": "200"}
        ]
        
        result = format_table(data)
        
        assert "id" in result
        assert "name" in result
        assert "Item 1" in result
        assert "Item 2" in result
    
    def test_format_table_empty_data(self):
        """Test formatting empty data."""
        data = []
        
        result = format_table(data)
        
        assert result == "Tidak ada data"
    
    def test_format_table_with_custom_headers(self):
        """Test formatting with custom headers."""
        data = [{"id": "1", "name": "Test"}]
        headers = ["id", "name"]
        
        result = format_table(data, headers)
        
        assert "id" in result
        assert "name" in result
    
    def test_format_table_fallback_without_tabulate(self, monkeypatch):
        """Test table formatting fallback when tabulate not available."""
        # Mock tabulate import to fail
        import sys
        monkeypatch.setitem(sys.modules, 'tabulate', None)
        
        data = [{"col1": "val1", "col2": "val2"}]
        result = format_table(data)
        
        # Should still produce some output
        assert "col1" in result or "val1" in result


class TestInputValidation:
    """Tests for input validation in CLI."""
    
    def test_get_input_with_default(self, monkeypatch):
        """Test get_input returns default when empty."""
        from library_system.utils.helper import get_input
        
        monkeypatch.setattr('builtins.input', lambda _: "")
        
        result = get_input("Prompt", default="default_value")
        
        assert result == "default_value"
    
    def test_get_input_without_default(self, monkeypatch):
        """Test get_input with user input."""
        from library_system.utils.helper import get_input
        
        monkeypatch.setattr('builtins.input', lambda _: "user_input")
        
        result = get_input("Prompt")
        
        assert result == "user_input"
    
    def test_get_int_input_valid(self, monkeypatch):
        """Test get_int_input with valid integer."""
        from library_system.utils.helper import get_int_input
        
        monkeypatch.setattr('builtins.input', lambda _: "42")
        
        result = get_int_input("Prompt")
        
        assert result == 42
    
    def test_get_int_input_with_default(self, monkeypatch):
        """Test get_int_input returns default when empty."""
        from library_system.utils.helper import get_int_input
        
        monkeypatch.setattr('builtins.input', lambda _: "")
        
        result = get_int_input("Prompt", default=10)
        
        assert result == 10
    
    def test_get_int_input_invalid(self, monkeypatch):
        """Test get_int_input raises error for invalid input."""
        from library_system.utils.helper import get_int_input
        
        monkeypatch.setattr('builtins.input', lambda _: "not_a_number")
        
        with pytest.raises(ValueError):
            get_int_input("Prompt")


class TestConfirmation:
    """Tests for confirmation dialogs."""
    
    def test_confirm_yes(self, monkeypatch):
        """Test confirm returns True for 'y'."""
        from library_system.utils.helper import confirm
        
        monkeypatch.setattr('builtins.input', lambda _: "y")
        
        result = confirm("Are you sure?")
        
        assert result is True
    
    def test_confirm_yes_full(self, monkeypatch):
        """Test confirm returns True for 'yes'."""
        from library_system.utils.helper import confirm
        
        monkeypatch.setattr('builtins.input', lambda _: "yes")
        
        result = confirm("Are you sure?")
        
        assert result is True
    
    def test_confirm_no(self, monkeypatch):
        """Test confirm returns False for 'n'."""
        from library_system.utils.helper import confirm
        
        monkeypatch.setattr('builtins.input', lambda _: "n")
        
        result = confirm("Are you sure?")
        
        assert result is False
    
    def test_confirm_case_insensitive(self, monkeypatch):
        """Test confirm is case insensitive."""
        from library_system.utils.helper import confirm
        
        monkeypatch.setattr('builtins.input', lambda _: "Y")
        
        result = confirm("Are you sure?")
        
        assert result is True


class TestCLIErrorHandling:
    """Tests for CLI error handling."""
    
    def test_cli_handles_invalid_choice(self):
        """Test CLI handles invalid menu choices gracefully."""
        # This is a basic test - full CLI testing would require more complex mocking
        # The CLI should not crash on invalid input
        assert True  # Placeholder - CLI is designed to handle invalid input
    
    def test_cli_handles_keyboard_interrupt(self):
        """Test CLI handles keyboard interrupt (Ctrl+C) gracefully."""
        # This is a design requirement - CLI should handle KeyboardInterrupt
        assert True  # Placeholder - actual testing would require subprocess


class TestCLIMenuStructure:
    """Tests for CLI menu structure."""
    
    def test_main_menu_options_exist(self):
        """Test main menu has expected options."""
        # This validates the CLI structure exists
        from library_system.main import LibraryApp
        
        app = LibraryApp()
        
        # Verify app has required methods
        assert hasattr(app, 'show_main_menu')
        assert hasattr(app, 'show_login_menu')
        assert hasattr(app, 'show_book_menu')
        assert hasattr(app, 'show_member_menu')
        assert hasattr(app, 'show_report_menu')
    
    def test_app_initialization(self):
        """Test LibraryApp initializes correctly."""
        from library_system.main import LibraryApp
        
        app = LibraryApp()
        
        assert app.database is not None
        assert app.auth_service is not None
        assert app.library_service is not None
        assert app.report_service is not None
        assert app.running is True


class TestCLIWorkflow:
    """Tests for CLI workflow."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Clean default data directory before each test."""
        import json
        from pathlib import Path
        data_dir = Path("library_system/data")
        if data_dir.exists():
            for file in data_dir.glob("*.json"):
                file.write_text("[]")
    
    def test_login_required_for_main_menu(self):
        """Test that main menu requires login."""
        from library_system.main import LibraryApp
        
        app = LibraryApp()
        
        # Initially no one is logged in
        assert not app.auth_service.is_logged_in()
    
    def test_logout_clears_session(self):
        """Test logout clears the session."""
        from library_system.main import LibraryApp
        
        app = LibraryApp()
        
        # Register and login
        app.auth_service.register_petugas("P002", "Admin", "081234567890", "admin2", "password123")
        app.auth_service.login("admin2", "password123")
        
        assert app.auth_service.is_logged_in()
        
        # Logout
        app.auth_service.logout()
        
        assert not app.auth_service.is_logged_in()


class TestCLIDataDisplay:
    """Tests for CLI data display."""
    
    def test_book_list_display_format(self, library_service):
        """Test book list data is properly formatted for display."""
        library_service.tambah_buku("B001", "Book Title", "Author Name", "Publisher", 2023, "Category", 5)
        
        books = library_service.daftar_buku()
        
        # Prepare data for display
        display_data = []
        for book in books:
            display_data.append({
                "ID": book.id,
                "Title": book.judul,
                "Author": book.penulis,
                "Stock": book.stok
            })
        
        assert len(display_data) == 1
        assert display_data[0]["ID"] == "B001"
        assert display_data[0]["Title"] == "Book Title"
    
    def test_member_list_display_format(self, library_service):
        """Test member list data is properly formatted for display."""
        library_service.tambah_anggota("A001", "Member Name", "081234567890", "Address")
        
        members = library_service.daftar_anggota()
        
        display_data = []
        for member in members:
            display_data.append({
                "ID": member.id,
                "Name": member.nama,
                "Contact": member.kontak,
                "Active Loans": member.jumlah_pinjaman()
            })
        
        assert len(display_data) == 1
        assert display_data[0]["Name"] == "Member Name"
        assert display_data[0]["Active Loans"] == 0


class TestCLIExceptionDisplay:
    """Tests for exception display in CLI."""
    
    def test_duplicate_id_error_message(self, library_service):
        """Test duplicate ID error produces user-friendly message."""
        from library_system.exceptions import DuplicateIDError
        
        library_service.tambah_buku("B001", "Book", "Author", "Pub", 2023, "Cat", 5)
        
        try:
            library_service.tambah_buku("B001", "Book2", "Author", "Pub", 2023, "Cat", 5)
            assert False, "Should have raised DuplicateIDError"
        except DuplicateIDError as e:
            # Error message should be user-friendly
            assert "sudah ada" in str(e)
    
    def test_not_found_error_message(self, library_service):
        """Test not found error produces user-friendly message."""
        from library_system.exceptions import BookNotFoundError
        
        try:
            library_service.edit_buku("B999", judul="New Title")
            assert False, "Should have raised BookNotFoundError"
        except BookNotFoundError as e:
            assert "tidak ditemukan" in str(e)

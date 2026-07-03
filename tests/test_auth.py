"""
Tests for AuthService.
"""

import pytest
from library_system.services import AuthService
from library_system.exceptions import (
    AuthenticationError,
    DuplicateIDError,
    InvalidInputError
)


class TestAuthServiceRegistration:
    """Tests for staff registration."""
    
    def test_register_staff_success(self, auth_service):
        """Test successful staff registration."""
        staff = auth_service.register_petugas(
            id="P001",
            nama="John Doe",
            kontak="081234567890",
            username="johndoe",
            password="password123"
        )
        
        assert staff.id == "P001"
        assert staff.nama == "John Doe"
        assert staff.username == "johndoe"
        assert len(staff.password_hash) == 64  # SHA256 hash length
    
    def test_register_duplicate_id(self, auth_service, sample_staff):
        """Test registration with duplicate ID."""
        with pytest.raises(DuplicateIDError, match="ID petugas .* sudah terdaftar"):
            auth_service.register_petugas(
                id="P001",
                nama="Another User",
                kontak="081234567899",
                username="anotheruser",
                password="password123"
            )
    
    def test_register_duplicate_username(self, auth_service, sample_staff):
        """Test registration with duplicate username."""
        with pytest.raises(DuplicateIDError, match="Username .* sudah digunakan"):
            auth_service.register_petugas(
                id="P002",
                nama="Another User",
                kontak="081234567899",
                username="testadmin",
                password="password123"
            )
    
    def test_register_short_password(self, auth_service):
        """Test registration with password less than 8 characters."""
        with pytest.raises(InvalidInputError, match="Password minimal 8 karakter"):
            auth_service.register_petugas(
                id="P001",
                nama="John Doe",
                kontak="081234567890",
                username="johndoe",
                password="pass"
            )


class TestAuthServiceLogin:
    """Tests for staff login."""
    
    def test_login_success(self, auth_service, sample_staff):
        """Test successful login."""
        user = auth_service.login("testadmin", "password123")
        
        assert user.username == "testadmin"
        assert auth_service.is_logged_in()
        assert auth_service.get_current_user() == user
    
    def test_login_wrong_username(self, auth_service, sample_staff):
        """Test login with non-existent username."""
        with pytest.raises(AuthenticationError, match="Username tidak ditemukan"):
            auth_service.login("wronguser", "password123")
    
    def test_login_wrong_password(self, auth_service, sample_staff):
        """Test login with incorrect password."""
        with pytest.raises(AuthenticationError, match="Password salah"):
            auth_service.login("testadmin", "wrongpassword")
    
    def test_login_empty_username(self, auth_service):
        """Test login with empty username."""
        with pytest.raises(InvalidInputError, match="Username tidak boleh kosong"):
            auth_service.login("", "password123")
    
    def test_login_empty_password(self, auth_service, sample_staff):
        """Test login with empty password."""
        with pytest.raises(InvalidInputError, match="Password tidak boleh kosong"):
            auth_service.login("testadmin", "")


class TestAuthServiceLogout:
    """Tests for staff logout."""
    
    def test_logout_success(self, auth_service, sample_staff):
        """Test successful logout."""
        auth_service.login("testadmin", "password123")
        auth_service.logout()
        
        assert not auth_service.is_logged_in()
        assert auth_service.get_current_user() is None
    
    def test_logout_without_login(self, auth_service):
        """Test logout when no one is logged in."""
        with pytest.raises(AuthenticationError, match="Tidak ada user yang sedang login"):
            auth_service.logout()


class TestAuthServiceHelpers:
    """Tests for helper methods."""
    
    def test_is_logged_in_false(self, auth_service):
        """Test is_logged_in returns False when no user logged in."""
        assert not auth_service.is_logged_in()
    
    def test_is_logged_in_true(self, auth_service, sample_staff):
        """Test is_logged_in returns True when user logged in."""
        auth_service.login("testadmin", "password123")
        assert auth_service.is_logged_in()
    
    def test_get_all_petugas(self, auth_service, sample_staff):
        """Test getting all registered staff."""
        auth_service.register_petugas(
            id="P002",
            nama="Jane Doe",
            kontak="081234567899",
            username="janedoe",
            password="password456"
        )
        
        staff_list = auth_service.get_all_petugas()
        assert len(staff_list) == 2

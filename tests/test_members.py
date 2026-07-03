"""
Tests for Member Management.
"""

import pytest
from library_system.exceptions import (
    MemberNotFoundError,
    DuplicateIDError,
    InvalidInputError
)


class TestMemberAdd:
    """Tests for adding members."""
    
    def test_add_member_success(self, library_service):
        """Test successfully adding a member."""
        member = library_service.tambah_anggota(
            id="A001",
            nama="John Doe",
            kontak="081234567890",
            alamat="Jl. Test No. 1"
        )
        
        assert member.id == "A001"
        assert member.nama == "John Doe"
        assert member.kontak == "081234567890"
        assert member.alamat == "Jl. Test No. 1"
    
    def test_add_member_duplicate_id(self, library_service, sample_member):
        """Test adding member with duplicate ID."""
        with pytest.raises(DuplicateIDError, match="Anggota dengan ID .* sudah ada"):
            library_service.tambah_anggota(
                id="A001",
                nama="Jane Doe",
                kontak="081234567899",
                alamat="Address"
            )
    
    def test_add_member_empty_name(self, library_service):
        """Test adding member with empty name."""
        with pytest.raises(ValueError, match="Nama tidak boleh kosong"):
            library_service.tambah_anggota(
                id="A001",
                nama="",
                kontak="081234567890",
                alamat="Address"
            )


class TestMemberEdit:
    """Tests for editing members."""
    
    def test_edit_member_name(self, library_service, sample_member):
        """Test editing member name."""
        updated = library_service.edit_anggota("A001", nama="Updated Name")
        
        assert updated.nama == "Updated Name"
        assert updated.kontak == "081234567891"  # Unchanged
    
    def test_edit_member_multiple_fields(self, library_service, sample_member):
        """Test editing multiple member fields."""
        updated = library_service.edit_anggota(
            "A001",
            nama="New Name",
            kontak="081999999999",
            alamat="New Address"
        )
        
        assert updated.nama == "New Name"
        assert updated.kontak == "081999999999"
        assert updated.alamat == "New Address"
    
    def test_edit_member_not_found(self, library_service):
        """Test editing non-existent member."""
        with pytest.raises(MemberNotFoundError, match="Anggota dengan ID .* tidak ditemukan"):
            library_service.edit_anggota("A999", nama="Name")
    
    def test_edit_member_empty_name(self, library_service, sample_member):
        """Test editing member with empty name."""
        with pytest.raises(InvalidInputError, match="Nama tidak boleh kosong"):
            library_service.edit_anggota("A001", nama="")


class TestMemberDelete:
    """Tests for deleting members."""
    
    def test_delete_member_success(self, library_service, sample_member):
        """Test successfully deleting a member."""
        library_service.hapus_anggota("A001")
        
        members = library_service.daftar_anggota()
        assert len(members) == 0
    
    def test_delete_member_not_found(self, library_service):
        """Test deleting non-existent member."""
        with pytest.raises(MemberNotFoundError, match="Anggota dengan ID .* tidak ditemukan"):
            library_service.hapus_anggota("A999")
    
    def test_delete_member_with_active_loan(self, library_service, sample_loan):
        """Test deleting member with active loans."""
        with pytest.raises(InvalidInputError, match="masih memiliki pinjaman aktif"):
            library_service.hapus_anggota("A001")


class TestMemberSearch:
    """Tests for searching members."""
    
    def test_search_member_by_name(self, library_service):
        """Test searching members by name."""
        library_service.tambah_anggota("A001", "John Doe", "081111111111", "Address 1")
        library_service.tambah_anggota("A002", "Jane Smith", "081222222222", "Address 2")
        
        results = library_service.cari_anggota("John")
        
        assert len(results) == 1
        assert results[0].nama == "John Doe"
    
    def test_search_member_by_contact(self, library_service):
        """Test searching members by contact."""
        library_service.tambah_anggota("A001", "John Doe", "081111111111", "Address")
        library_service.tambah_anggota("A002", "Jane Smith", "082222222222", "Address")
        
        results = library_service.cari_anggota("0811")
        
        assert len(results) == 1
        assert results[0].kontak == "081111111111"
    
    def test_search_member_case_insensitive(self, library_service, sample_member):
        """Test case-insensitive member search."""
        results = library_service.cari_anggota("test")
        
        assert len(results) == 1
    
    def test_search_member_no_results(self, library_service, sample_member):
        """Test member search with no results."""
        results = library_service.cari_anggota("NonExistent")
        
        assert len(results) == 0


class TestMemberList:
    """Tests for listing members."""
    
    def test_list_all_members(self, library_service):
        """Test listing all members."""
        library_service.tambah_anggota("A001", "Member 1", "081111111111", "Address 1")
        library_service.tambah_anggota("A002", "Member 2", "082222222222", "Address 2")
        
        members = library_service.daftar_anggota()
        
        assert len(members) == 2
    
    def test_list_members_empty(self, library_service):
        """Test listing members when none exist."""
        members = library_service.daftar_anggota()
        
        assert len(members) == 0


class TestMemberLoanTracking:
    """Tests for member loan tracking."""
    
    def test_member_loan_count_zero(self, library_service, sample_member):
        """Test member with no loans."""
        member = library_service._find_anggota_by_id("A001")
        
        assert member.jumlah_pinjaman() == 0
    
    def test_member_loan_count_one(self, library_service, sample_loan):
        """Test member with one active loan."""
        member = library_service._find_anggota_by_id("A001")
        
        assert member.jumlah_pinjaman() == 1
    
    def test_member_loan_count_after_return(self, library_service, sample_loan):
        """Test member loan count after return."""
        library_service.kembalikan_buku(sample_loan.id)
        
        member = library_service._find_anggota_by_id("A001")
        assert member.jumlah_pinjaman() == 0

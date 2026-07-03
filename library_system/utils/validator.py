"""
Module untuk Validator.

Module ini menyediakan fungsi-fungsi validasi input.
"""

from typing import Any
from ..exceptions import InvalidInputError


def validate_non_empty_string(value: str, field_name: str) -> None:
    """
    Validasi bahwa string tidak kosong.
    
    Args:
        value: String yang akan divalidasi
        field_name: Nama field untuk error message
        
    Raises:
        InvalidInputError: Jika string kosong atau hanya whitespace
    """
    if not value or not value.strip():
        raise InvalidInputError(f"{field_name} tidak boleh kosong")


def validate_positive_integer(value: int, field_name: str) -> None:
    """
    Validasi bahwa nilai adalah integer positif atau nol.
    
    Args:
        value: Integer yang akan divalidasi
        field_name: Nama field untuk error message
        
    Raises:
        InvalidInputError: Jika nilai negatif
    """
    if value < 0:
        raise InvalidInputError(f"{field_name} tidak boleh negatif")


def validate_integer_type(value: Any, field_name: str) -> None:
    """
    Validasi bahwa nilai adalah integer.
    
    Args:
        value: Nilai yang akan divalidasi
        field_name: Nama field untuk error message
        
    Raises:
        InvalidInputError: Jika bukan integer
    """
    if not isinstance(value, int):
        raise InvalidInputError(f"{field_name} harus berupa integer")


def validate_password(password: str, min_length: int = 8) -> None:
    """
    Validasi password sesuai requirements.
    
    Args:
        password: Password yang akan divalidasi
        min_length: Panjang minimum password
        
    Raises:
        InvalidInputError: Jika password tidak memenuhi requirements
    """
    if len(password) < min_length:
        raise InvalidInputError(f"Password minimal {min_length} karakter")


def validate_id_format(id: str, field_name: str) -> None:
    """
    Validasi format ID.
    
    Args:
        id: ID yang akan divalidasi
        field_name: Nama field untuk error message
        
    Raises:
        InvalidInputError: Jika ID tidak valid
    """
    validate_non_empty_string(id, field_name)

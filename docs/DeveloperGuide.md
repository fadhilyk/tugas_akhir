# Developer Guide

Panduan untuk pengembang yang ingin memahami, memodifikasi, atau mengextend sistem.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Domain Models](#domain-models)
3. [Services](#services)
4. [Database Layer](#database-layer)
5. [Exceptions](#exceptions)
6. [Logging](#logging)
7. [Validation](#validation)
8. [Testing](#testing)
9. [How to Extend the System](#how-to-extend-the-system)

---

## Project Structure

```
library_system/          # Main application package
├── main.py             # CLI entry point
├── __init__.py
├── models/             # Domain models
├── services/           # Business logic
├── storage/            # Data persistence
├── utils/              # Utilities
├── exceptions/         # Custom exceptions
└── data/               # JSON storage
tests/                   # Test suite
docs/                    # Documentation
```

### Package Organization

Semua modul di dalam `library_system/` menggunakan relative imports untuk internal references:

```python
from ..models import Buku           # From services/ → models/
from ..storage.database import Database  # From services/ → storage/
from ..exceptions import *          # From services/ → exceptions/
```

---

## Domain Models

Package: `library_system/models/`

### Class Hierarchy

```
Pengguna (ABC, @dataclass)
├── Anggota (@dataclass)
└── Petugas (@dataclass)

Buku (@dataclass)
Peminjaman (@dataclass)
└── contains → Denda (@dataclass)
```

### Model Design Pattern

Semua model menggunakan Python `@dataclass` untuk mengurangi boilerplate:

```python
from dataclasses import dataclass, field

@dataclass
class Buku:
    id: str
    judul: str
    penulis: str
    penerbit: str
    tahun: int
    kategori: str
    stok: int
```

### Validation in Models

Validasi dilakukan di `__post_init__` untuk menjaga data invariants:

```python
def __post_init__(self) -> None:
    if not self.judul or not self.judul.strip():
        raise ValueError("Judul tidak boleh kosong")
    if self.stok < 0:
        raise ValueError("Stok tidak boleh negatif")
```

### Constants

Definisi konstanta dalam module masing-masing:

| Constant | Value | Location |
|---|---|---|
| `MAX_PINJAMAN` | 5 | `models/anggota.py` |
| `LAMA_PINJAM` | 7 | `models/peminjaman.py` |
| `DENDA_PER_HARI` | 2000 | `models/denda.py` |

### Adding a New Model

To add a new entity, e.g., `Kategori`:

1. Create `library_system/models/kategori.py`
2. Use `@dataclass` and implement `__post_init__` validation
3. Export in `models/__init__.py`

---

## Services

Package: `library_system/services/`

### AuthService

Responsible for staff authentication.

**Key Methods:**

| Method | Description |
|---|---|
| `register_petugas()` | Register new staff with hashed password |
| `login()` | Authenticate username/password |
| `logout()` | End current session |
| `is_logged_in()` | Check if any user is logged in |
| `get_current_user()` | Get currently logged in staff |

**Password Security:**

- Passwords are hashed using SHA256
- Plaintext passwords are never stored
- Validation requires minimum 8 characters

### LibraryService

Core business logic for all library operations.

**Key Methods:**

| Method | Description |
|---|---|
| `tambah_buku()` | Add new book |
| `edit_buku()` | Edit existing book (partial update) |
| `hapus_buku()` | Delete book (validates no active loan) |
| `cari_buku()` | Search books by keyword |
| `pinjam_buku()` | Process book borrowing |
| `kembalikan_buku()` | Process book return |

**Transaction Flow (Borrow):**

1. Validate member exists
2. Validate book exists and is available
3. Validate member hasn't reached max loan limit
4. Create Peminjaman object with auto-calculated due date
5. Reduce book stock
6. Add loan to member's active loans
7. Save all changes to database
8. Log the action

### ReportService

Generates various reports by reading from LibraryService.

**Key Methods:**

| Method | Description |
|---|---|
| `laporan_semua_buku()` | All books with availability status |
| `laporan_buku_tersedia()` | Books with stock > 0 |
| `laporan_buku_dipinjam()` | Books currently on loan |
| `laporan_anggota()` | All members with loan counts |
| `laporan_transaksi()` | All transactions (optional status filter) |
| `laporan_denda()` | All fines with details |
| `statistik_perpustakaan()` | General library statistics |

### Adding a New Service Method

To add a new feature, e.g., "book reservation":

1. Add method to `LibraryService`
2. Add validation logic using existing `_get_*_or_raise()` helpers
3. Use `self._database.save_*()` to persist changes
4. Use `self._logger` to log action
5. Wrap in try/except and re-raise custom exceptions

---

## Database Layer

Package: `library_system/storage/`

### Database Class

Single class handling all JSON I/O operations.

```python
class Database:
    def __init__(self, data_dir: str = "library_system/data"):
        self.data_dir = Path(data_dir)
        self.buku_file = ...
        self.anggota_file = ...
        self.petugas_file = ...
        self.transaksi_file = ...
```

### Public API

| Method | Input | Output |
|---|---|---|
| `load_buku()` | — | `list[Buku]` |
| `save_buku(list)` | `list[Buku]` | — |
| `load_anggota()` | — | `list[Anggota]` |
| `save_anggota(list)` | `list[Anggota]` | — |
| `load_petugas()` | — | `list[Petugas]` |
| `save_petugas(list)` | `list[Petugas]` | — |
| `load_transaksi()` | — | `list[Peminjaman]` |
| `save_transaksi(list)` | `list[Peminjaman]` | — |
| `backup(suffix)` | Optional suffix | Creates backup files |

### Internal Serialization

Every dataclass model has a pair of private serialization methods:

```python
def _serialize_buku(self, buku: Buku) -> dict[str, Any]:
def _deserialize_buku(self, data: dict[str, Any]) -> Buku:
```

**Serialization handling:**
- `datetime` → ISO 8601 string `.isoformat()`
- `datetime` (loading) → `datetime.fromisoformat()`
- Nested objects → Recursive serialization (Peminjaman → Denda)
- Optional fields → `.get()` with defaults

### Error Recovery

- **Corrupted JSON**: Returns empty `[]`, logs warning
- **Missing file**: Creates new `.json` with `[]`
- **Empty file**: Returns `[]`

### Switching to a Different Database

To replace JSON with SQLite:

1. Create `storage/database_sqlite.py`
2. Implement the same public API (`load_buku()`, `save_buku()`, etc.)
3. Pass the new database instance to services:

```python
db = SQLiteDatabase("library.db")
service = LibraryService(db)
```

---

## Exceptions

Package: `library_system/exceptions/`

### Exception Hierarchy

```
LibraryError (base, extends Exception)
├── AuthenticationError      — Login/logout failures
├── BookNotFoundError        — Book ID not found
├── MemberNotFoundError      — Member ID not found
├── LoanNotFoundError        — Loan ID not found
├── BookUnavailableError     — Stock empty
├── DuplicateIDError         — Duplicate ID/username
├── MaximumLoanReachedError  — Max 5 loans reached
├── InvalidInputError        — Validation failures
└── DatabaseError            — JSON storage errors
```

### Usage Pattern

```python
from ..exceptions import BookNotFoundError

def _get_buku_or_raise(self, buku_id: str) -> Buku:
    buku = self._find_buku_by_id(buku_id)
    if not buku:
        raise BookNotFoundError(f"Buku dengan ID '{buku_id}' tidak ditemukan")
    return buku
```

### Adding a New Exception

```python
class BookReservationError(LibraryError):
    """Raised when book reservation fails."""
    pass
```

---

## Logging

Package: `library_system/utils/logger.py`

### Configuration

```python
logger = setup_logger()  # Returns configured logger
```

**Log file:** `logs/library.log` (rotating, 5 MB per file, 5 backups)

**Log format:**
```
2026-07-03 14:30:00 - library_system - INFO - [ADD_BOOK] Book added: Python Programming (ID: B001)
```

### Log Actions

```python
log_action(logger, "BORROW_BOOK", "Member Alice borrowed 'Book X'")
log_error(logger, exception, "context_string")
```

### Logged Events

| Event | Action Tag |
|---|---|
| Staff registration | `REGISTER_STAFF` |
| Login | `LOGIN` |
| Logout | `LOGOUT` |
| Book added | `ADD_BOOK` |
| Book edited | `EDIT_BOOK` |
| Book deleted | `DELETE_BOOK` |
| Member added | `ADD_MEMBER` |
| Book borrowed | `BORROW_BOOK` |
| Book returned | `RETURN_BOOK` |
| Database save | `SAVE_DATA` |
| Database load | `LOAD_DATA` |
| Error | `ERROR` |

---

## Validation

Package: `library_system/utils/validator.py`

Centralized validation functions:

| Function | Description |
|---|---|
| `validate_non_empty_string(value, name)` | Ensures string is not blank |
| `validate_positive_integer(value, name)` | Ensures integer >= 0 |
| `validate_integer_type(value, name)` | Ensures value is int type |
| `validate_password(password, min_len)` | Minimum password length |
| `validate_id_format(id, name)` | Validates ID format |

All validators raise `InvalidInputError` on failure.

---

## Testing

See full documentation in [Testing.md](Testing.md).

---

## How to Extend the System

### Add a New Model (e.g., Publisher)

1. Create `library_system/models/penerbit.py`
2. Use `@dataclass`, implement `__post_init__`
3. Export in `models/__init__.py`

### Add a New Service Method (e.g., Book Reservation)

1. Add method in `LibraryService`
2. Add validation using existing helpers
3. Persist via `self._database`
4. Log via `self._logger`
5. Add test in `tests/test_books.py`

### Add a New Report

1. Add method in `ReportService`
2. Read data from `LibraryService`
3. Return `list[dict]`
4. Update CLI in `main.py` to add menu option
5. Add test in `tests/test_reports.py`

### Add a New CLI Menu

1. Add method in `LibraryApp` class (`main.py`)
2. Call appropriate service method
3. Handle exceptions with try/except
4. Add menu option in the relevant menu method

### Add a New Storage Backend

1. Create `storage/database_sqlite.py`
2. Implement same public API as `Database`
3. Pass to services via DI

### Coding Standards

- **PEP 8**: Follow Python style guide
- **Type Hints**: All public methods must have complete type hints
- **Docstrings**: Google-style docstrings for all classes and methods
- **DRY**: No duplicated code — extract into shared methods
- **Single Responsibility**: Each method does one thing
- **Test Coverage**: Every new feature must have tests

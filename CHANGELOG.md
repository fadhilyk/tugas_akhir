# Changelog

All notable changes to the Digital Library Management System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-07-03

### Added

#### Project Initialization
- Initial project structure with layered architecture
- Directory structure: `models/`, `services/`, `storage/`, `utils/`, `data/`
- `requirements.txt` with project dependencies
- `.gitignore` for Python projects

#### Domain Models
- `Pengguna` — Abstract base class using `abc.ABC`
- `Anggota` — Member with loan tracking (inherits Pengguna)
- `Petugas` — Staff with authentication (inherits Pengguna)
- `Buku` — Book with stock management
- `Peminjaman` — Loan transaction with due date calculation
- `Denda` — Fine calculation at Rp 2,000/day
- Constants: `MAX_PINJAMAN=5`, `LAMA_PINJAM=7`, `DENDA_PER_HARI=2000`
- OOP principles: abstraction, inheritance, encapsulation, polymorphism
- Type hints and dataclass usage throughout

#### Service Layer
- `AuthService` — Staff registration, login/logout, session management
- `LibraryService` — CRUD for books and members, borrow/return transactions
- `ReportService` — 7 report types with filtering capabilities
- SHA256 password hashing
- In-memory collections for temporary storage
- Full input validation with meaningful error messages

#### Persistent Storage Layer (JSON)
- `Database` class with full JSON serialization/deserialization
- Automatic file and directory creation
- Data persistence across application restarts
- Automatic save on every successful operation
- Backup functionality with timestamp
- Error recovery for corrupted or missing files
- ISO 8601 datetime serialization
- Nested object serialization (Peminjaman → Denda)

#### Interactive Command Line Interface (CLI)
- Login menu with registration option
- Main menu with 6 functional sections
- Book management submenu (add, edit, delete, search, list)
- Member management submenu (add, edit, delete, search, list)
- Borrow book with auto-calculated due dates
- Return book with fine calculation
- Reports menu with 7 report types
- Library statistics dashboard
- Formatted tables using tabulate (with fallback formatter)
- Clear screen navigation
- Confirmation dialogs for destructive actions
- Graceful error handling — no stack traces to users

#### Code Quality
- Custom exception hierarchy (`LibraryError` base + 9 subclasses)
- Rotating file logging (`logs/library.log`)
- Structured logging for all CRUD and auth operations
- Centralized validation functions (`utils/validator.py`)
- Refactored service layer with `_get_*_or_raise()` helper pattern
- Reduced code duplication in search methods
- Consistent try/except/log/raise pattern in all service methods

#### Automated Testing (pytest)
- 128 test cases across 7 test files
- Temporary directory fixtures for isolated testing
- Coverage: models (~95%), services (~95%), storage (~90%)
- All custom exceptions tested
- Authentication: register, login, logout, edge cases
- Books: full CRUD, search, availability
- Members: full CRUD, search, loan tracking
- Loans: borrow, return, fine calculation, max limit
- Reports: all 7 report types, filters, statistics
- Database: save/load, serialization, error recovery, backup
- CLI: helper functions, input validation, menu structure

#### CI/CD
- GitHub Actions workflow (`.github/workflows/python-ci.yml`)
- Automatic testing on push/PR to main
- Python 3.12 compilation check
- Full 128-test suite execution
- Coverage reporting

#### Documentation
- `README.md` — Full project documentation with Mermaid diagrams
- `docs/Architecture.md` — System architecture with 6 Mermaid diagrams
- `docs/UserGuide.md` — Complete user manual with examples
- `docs/DeveloperGuide.md` — Developer reference with extension guide
- `docs/Testing.md` — Test documentation and CI/CD explanation
- `CHANGELOG.md` — This file
- `LICENSE` — MIT License
- `CONTRIBUTING.md` — Contribution guidelines
- `CODE_OF_CONDUCT.md` — Contributor Covenant
- `SECURITY.md` — Security policy

### Technical Details

- **Language:** Python 3.12+
- **Architecture:** Clean/Layered Architecture
- **Storage:** JSON files with automatic persistence
- **Testing:** pytest, 128 tests
- **CI/CD:** GitHub Actions
- **Logging:** Rotating file handler, 5 MB per file, 5 backups

[1.0.0]: https://github.com/fadhilyk/tugas_akhir/releases/tag/v1.0.0

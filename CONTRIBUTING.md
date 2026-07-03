# Contributing to Digital Library Management System

Terima kasih atas minat Anda untuk berkontribusi pada proyek ini. Berikut adalah panduan untuk berkontribusi.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Branch Strategy](#branch-strategy)
3. [Commit Convention](#commit-convention)
4. [Pull Request Workflow](#pull-request-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing Requirements](#testing-requirements)
7. [Development Setup](#development-setup)

## Code of Conduct

Proyek ini menerapkan [Contributor Covenant](CODE_OF_CONDUCT.md). Dengan berpartisipasi, Anda diharapkan untuk menjunjung tinggi kode etik ini.

## Branch Strategy

```
main          → Production-ready code
  └── develop → Integration branch
       ├── feat/feature-name   → New features
       ├── fix/bug-name        → Bug fixes
       ├── refactor/name       → Code refactoring
       └── docs/name           → Documentation updates
```

### Branch Naming

| Prefix | Purpose | Example |
|---|---|---|
| `feat/` | New feature | `feat/book-reservation` |
| `fix/` | Bug fix | `fix/negative-stock-bug` |
| `refactor/` | Code refactoring | `refactor/validator-module` |
| `docs/` | Documentation | `docs/api-docs` |
| `test/` | Testing | `test/coverage-improvement` |
| `chore/` | Maintenance | `chore/update-dependencies` |

## Commit Convention

Gunakan [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>: <short description>

[optional body]
[optional footer]
```

### Types

| Type | Usage |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code refactoring |
| `test` | Adding or modifying tests |
| `docs` | Documentation changes |
| `chore` | Maintenance, dependencies, CI |
| `style` | Formatting, linting (no logic change) |

### Examples

```
feat: add book reservation feature
fix: handle negative stock validation
refactor: extract validation to centralized module
test: add unit tests for auth service
docs: update API documentation
chore: update pytest to v9.0
```

## Pull Request Workflow

### Before Submitting

1. Branch from `develop` (or `main` for hotfixes)
2. Implement your changes following coding standards
3. Add tests for new functionality
4. Run the full test suite: `pytest`
5. Ensure compilation passes: `python -m compileall library_system`
6. Update documentation if needed

### PR Checklist

- [ ] Code follows project coding standards
- [ ] Tests added/updated for new functionality
- [ ] All tests pass
- [ ] Compilation check passes
- [ ] Documentation updated (if applicable)
- [ ] Changelog updated (if applicable)
- [ ] No `print()` statements left in production code
- [ ] No debug logging in production code

### Review Process

1. Open PR against `develop` branch
2. CI pipeline runs automatically
3. Maintainer reviews code
4. Address review feedback
5. Squash merge to `develop`
6. Periodic merge `develop` → `main` for releases

## Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Line length: 100 characters
- Use 4 spaces for indentation (no tabs)

### Type Hints

Semua public functions dan methods **wajib** memiliki type hints:

```python
def tambah_buku(self, id: str, judul: str, stok: int) -> Buku:
    ...
```

### Docstrings

Gunakan Google-style docstrings:

```python
def pinjam_buku(self, anggota_id: str, buku_id: str) -> Peminjaman:
    """
    Memproses peminjaman buku oleh anggota.
    
    Args:
        anggota_id: ID anggota yang meminjam
        buku_id: ID buku yang dipinjam
        
    Returns:
        Object Peminjaman yang baru dibuat
        
    Raises:
        BookNotFoundError: Jika buku tidak ditemukan
    """
```

### Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Classes | PascalCase | `LibraryService` |
| Functions/Methods | snake_case | `tambah_buku()` |
| Variables | snake_case | `buku_list` |
| Constants | UPPER_CASE | `MAX_PINJAMAN` |
| Private attributes | `_` prefix | `self._buku_list` |
| Protected methods | `_` prefix | `self._find_buku_by_id()` |
| Modules | snake_case | `auth_service.py` |

### Architecture Rules

- Presentation layer (CLI) tidak boleh langsung mengakses Database
- Service layer adalah satu-satunya yang boleh memanggil Database
- Models tidak boleh bergantung pada layer manapun
- Semua operasi CRUD harus melalui Service Layer
- Gunakan custom exceptions (`exceptions/`), bukan `ValueError`

## Testing Requirements

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=library_system

# Run specific test file
pytest tests/test_auth.py -v
```

### Test Coverage

- Setiap public method harus memiliki minimal 2 test: happy path + error path
- Test harus menggunakan fixtures dari `conftest.py`
- Jangan menggunakan data directory default — gunakan `temp_data_dir` fixture
- Test harus independen — tidak bergantung pada urutan eksekusi

### What to Test

1. **Happy path** — Operasi normal berhasil
2. **Error path** — Input invalid raise correct exception
3. **Edge cases** — Data kosong, boundary values, duplicates
4. **State changes** — Stock, pinjaman count, status
5. **Persistence** — Data survive across instances

## Development Setup

```bash
# Clone repository
git clone https://github.com/fadhilyk/tugas_akhir.git
cd tugas_akhir

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run application
python library_system/main.py
```

## Questions?

Jika ada pertanyaan, silakan buka issue di repository GitHub.

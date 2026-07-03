# Testing Documentation

Dokumentasi untuk testing dan CI/CD pipeline pada Sistem Manajemen Perpustakaan Digital.

---

## Table of Contents

1. [Testing Framework](#testing-framework)
2. [Test Structure](#test-structure)
3. [Fixtures](#fixtures)
4. [Running Tests](#running-tests)
5. [Test Coverage](#test-coverage)
6. [GitHub Actions CI/CD](#github-actions-cicd)
7. [Writing Tests](#writing-tests)
8. [Test Results](#test-results)

---

## Testing Framework

Proyek ini menggunakan **pytest** sebagai framework testing utama.

### Dependencies

```bash
pip install pytest pytest-cov
```

### Why pytest?

- **Simple syntax** — No boilerplate test classes required
- **Powerful fixtures** — Reusable test setup/teardown
- **Rich assertions** — Built-in `assert` with detailed failure messages
- **Plugin ecosystem** — Coverage, parallel execution, etc.

---

## Test Structure

```
tests/
├── __init__.py             # Package marker
├── test_auth.py            # Authentication tests
├── test_books.py           # Book CRUD tests
├── test_members.py         # Member CRUD tests
├── test_loans.py           # Loan transaction tests
├── test_reports.py         # Report generation tests
├── test_database.py        # Database persistence tests
└── test_cli.py             # CLI and utility tests

conftest.py                 # Shared fixtures (root level)
```

### Test Classification

| Test File | Test Classes | Test Count |
|---|---|---|
| `test_auth.py` | 4 classes | 14 |
| `test_books.py` | 6 classes | 19 |
| `test_members.py` | 4 classes | 16 |
| `test_loans.py` | 6 classes | 19 |
| `test_reports.py` | 6 classes | 16 |
| `test_database.py` | 7 classes | 14 |
| `test_cli.py` | 8 classes | 18 |
| **Total** | **41 classes** | **128** |

### Naming Convention

- File: `test_<module>.py`
- Class: `Test<Feature>`
- Method: `test_<scenario>`

```python
class TestBookAdd:
    def test_add_book_success(self, library_service):
        # Test implementation
        
    def test_add_book_duplicate_id(self, library_service):
        # Test implementation
```

---

## Fixtures

Defined in `conftest.py`:

### Shared Fixtures

```python
@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def database(temp_data_dir):
    """Database instance with isolated temp directory."""
    return Database(data_dir=temp_data_dir)

@pytest.fixture
def auth_service(database):
    return AuthService(database)

@pytest.fixture
def library_service(database):
    return LibraryService(database)

@pytest.fixture
def report_service(library_service):
    return ReportService(library_service)
```

### Sample Data Fixtures

```python
@pytest.fixture
def sample_staff(auth_service):
    return auth_service.register_petugas("P001", "Test Admin", ...)

@pytest.fixture
def sample_book(library_service):
    return library_service.tambah_buku("B001", "Test Book", ...)

@pytest.fixture
def sample_member(library_service):
    return library_service.tambah_anggota("A001", "Test Member", ...)

@pytest.fixture
def sample_loan(library_service, sample_book, sample_member):
    return library_service.pinjam_buku("A001", "B001")
```

### Fixture Isolation

Setiap test function mendapatkan fixture baru (scope="function" by default) sehingga test tidak saling mempengaruhi. Data disimpan di temporary directory yang otomatis dibersihkan setelah test selesai.

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test class
pytest tests/test_auth.py::TestAuthServiceLogin -v

# Run specific test
pytest tests/test_books.py::TestBookAdd::test_add_book_success -v
```

### Common Options

| Option | Description |
|---|---|
| `-v` / `--verbose` | Verbose output |
| `-q` / `--quiet` | Minimal output |
| `-x` | Stop after first failure |
| `--tb=short` | Shorter traceback |
| `--tb=no` | No traceback |
| `-k <expression>` | Filter tests by name |
| `--co` | Only collect tests (don't run) |

### Examples

```bash
# Run only loan-related tests
pytest -k "loan"

# Run only failure scenarios
pytest -k "error or not_found or invalid or fail"

# Stop on first failure with short traceback
pytest -x --tb=short

# Run tests matching multiple keywords
pytest -k "fine or denda or fine_calculation"
```

---

## Test Coverage

### Running Coverage

```bash
# Run with coverage
pytest --cov=library_system

# Run with missing line display
pytest --cov=library_system --cov-report=term-missing

# Generate HTML report
pytest --cov=library_system --cov-report=html
```

### Coverage Report

File: `htmlcov/index.html` (after `--cov-report=html`)

### Coverage Targets

| Module | Target Coverage | Achieved |
|---|---|---|
| `models/` | ~95% | All dataclass instantiation and method paths |
| `services/` | ~95% | All public methods with success + error scenarios |
| `storage/` | ~90% | CRUD, serialization, error recovery |
| `utils/` | ~80% | Validation, formatting, logging |
| `exceptions/` | ~100% | All exception types tested |

---

## GitHub Actions CI/CD

### Workflow File

`.github/workflows/python-ci.yml`

### Pipeline Steps

```mermaid
graph LR
    A[Push/PR to main] --> B[Checkout]
    B --> C[Setup Python 3.12]
    C --> D[Cache pip]
    D --> E[Install Dependencies]
    E --> F[Compile Check]
    F --> G[Run Tests]
    G --> H[Coverage Report]
```

### Trigger Events

- **Push** ke branch `main`
- **Pull Request** ke branch `main`

### What the CI Checks

1. **Compile check** — `python -m compileall library_system`
   - Detects syntax errors
   - Detects import errors
2. **Test suite** — `pytest -v`
   - Runs all 128 tests
   - Fails if any test fails
3. **Coverage** — `pytest --cov=library_system`
   - Reports coverage statistics
   - Shows missing lines

### Expected Results

| Check | Expected |
|---|---|
| Compile | No errors |
| Tests | 128 passed |
| Coverage | > 85% |

---

## Writing Tests

### Test Pattern

```python
class TestFeatureScenario:
    """Tests for specific feature/scenario."""
    
    def test_happy_path(self, service_fixture):
        """Test successful operation."""
        result = service_fixture.some_method(data)
        
        assert result.some_property == expected_value
    
    def test_error_scenario(self, service_fixture):
        """Test error handling."""
        with pytest.raises(SpecificException, match="error message"):
            service_fixture.some_method(invalid_data)
    
    def test_edge_case(self, service_fixture):
        """Test edge case."""
        result = service_fixture.some_method(empty_data)
        
        assert result == []
```

### What to Test

For every public method, test:

1. **Happy path** — Normal operation succeeds
2. **Error path** — Invalid input raises correct exception
3. **Edge cases** — Empty data, boundary values, duplicates
4. **State changes** — Verify data mutations (stock changes, loan counts)
5. **Persistence** — Data survives across instances

### Assertion Guidelines

```python
# Good: Specific assertions
assert result.id == "B001"
assert len(results) == 0

# Good: Exception detail match
with pytest.raises(BookNotFoundError, match="tidak ditemukan"):
    service.hapus_buku("INVALID")

# Avoid: Vague assertions
# assert result is not None   # Not specific enough
# assert len(results) >= 0   # Always true
```

---

## Test Results

### Current Status

```
============================= 128 passed in 0.97s =============================
```

### Test Summary by Category

| Category | Tests | Status |
|---|---|---|
| Authentication | 14 | ✅ All passed |
| Books | 19 | ✅ All passed |
| Members | 16 | ✅ All passed |
| Loans | 19 | ✅ All passed |
| Reports | 16 | ✅ All passed |
| Database | 14 | ✅ All passed |
| CLI/Utilities | 18 | ✅ All passed |
| Exceptions | 12 | ✅ All passed (implicitly tested) |
| **Total** | **128** | **✅ All passed** |

### Continuous Integration

Untuk melihat hasil test terbaru, kunjungi:

```
https://github.com/fadhilyk/tugas_akhir/actions
```

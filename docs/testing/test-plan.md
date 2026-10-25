# Glasswave Desktop Test Plan

## 1. Test Strategy
Testing spans static analysis, asset schema validation, unit logic tests, integration tests, installer idempotence checks, and ADR traceability audits.

## 2. Test Suites
- **Configuration & State:**
  - `tests/test_config.py`: Schema validation, default fallback, corruption recovery, atomic writes, backup generation, CLI commands.
- **Calculator Math Engine:**
  - `tests/test_calculator.py`: Basic arithmetic, operator precedence, division by zero, float precision, and AST security (rejection of malicious python injection).
- **File Manager Operations:**
  - `tests/test_file_operations.py`: Path traversal protection, FreeDesktop trash compliance, directory enumeration, rename/copy/cut/paste mechanics.
- **System Monitor Engine:**
  - `tests/test_system_monitor.py`: Linux `/proc/stat`, `/proc/meminfo`, and `/proc/[pid]/` parsing, honest permission handling, metric bounds.
- **Installer & Rollback:**
  - `tests/test_installer.py`: Dry-run execution, user vs system paths, manifest tracking, configuration backup creation, clean rollback.
- **Desktop Assets & Metadata:**
  - `tests/test_desktop_assets.py`: FreeDesktop `.desktop` file syntax, icon theme `index.theme`, Plasma `metadata.json`, color scheme INI syntax, spec file validation.
- **ADR Coverage Audit:**
  - `tests/test_adr_coverage.py`: Verifies that 100% of non-generated implementation files are documented in an accepted ADR.

## 3. Running Tests
Execute:
```bash
./scripts/run-tests.sh
```
All tests must pass before commits or releases.

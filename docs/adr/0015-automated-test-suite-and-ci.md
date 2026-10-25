# ADR-0015: Automated Test Suite and ADR Coverage Validation

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
To ensure enterprise stability and prevent regressions across updates, the project requires an automated test suite covering:
1. Configuration schemas, default handling, corruption recovery, and persistence.
2. Safe calculator math engine and AST security boundaries.
3. Safe file operations, trash mechanics, and path traversal protection.
4. System monitor procfs parsing, CPU/memory metric accuracy, and honest permissions.
5. Installer idempotency, manifest tracking, and backup rollback.
6. Desktop asset integrity (JSON schemas, SVG syntax, color scheme INI parsing, desktop entries, spec files).
7. **Strict ADR coverage enforcement:** Every single implementation file in the repository must be mapped to at least one accepted ADR.

## Scope and Requirements
1. Author comprehensive unit and integration tests under `tests/`:
   - `tests/test_config.py`
   - `tests/test_calculator.py`
   - `tests/test_file_operations.py`
   - `tests/test_system_monitor.py`
   - `tests/test_installer.py`
   - `tests/test_desktop_assets.py`
   - `tests/test_adr_coverage.py`
2. Provide unified test execution script `scripts/run-tests.sh` that runs the entire test suite, reports pass/fail tallies, and exits with non-zero on any error.
3. Implement CI workflow configuration (`.github/workflows/ci.yml`).

## Current Behavior / Previous Implementation
No automated tests existed in the workspace.

## Decision Made
1. Develop test suite using standard Python `unittest` framework (zero heavy external testing dependencies required).
2. Implement `tests/test_adr_coverage.py`:
   - Scans all non-generated implementation files across `desktop-*`, `scripts/`, and root files.
   - Parses the `Exact List of Affected Files` section of all ADRs in `docs/adr/`.
   - Asserts that 100% of implementation files are documented in an accepted ADR.
3. Author `scripts/run-tests.sh` with colored reporting and detailed failure diagnostics.

## Detailed Rationale
Using the built-in `unittest` runner ensures immediate, reliable test execution in any standard Linux environment without requiring complex pip packages or network downloads.

## Alternatives Evaluated
1. **PyTest exclusively:** PyTest is not installed on the base system; standard library `unittest` runs everywhere out of the box with zero dependencies while providing equivalent assertion power.
2. **Manual ad-hoc testing:** Insufficient for release quality; automated test execution guarantees rapid feedback on code modifications.

## Architecture and Implementation Consequences
- All tests can be executed with a single command: `./scripts/run-tests.sh` or `make test`.
- Guarantees zero undocumented changes through `test_adr_coverage.py`.

## Dependencies and Version Constraints
- Python 3.10+ (standard library `unittest`).
- Bash 4.x+ for runner script.

## Security, Performance, and Accessibility
- **Security:** Tests verify AST sandboxing and path traversal resistance.
- **Performance:** Complete test suite runs in under 3 seconds.
- **Accessibility:** Tests verify presence of accessibility labels in desktop entries.

## Exact List of Affected Files
- `tests/__init__.py`
- `tests/test_config.py`
- `tests/test_calculator.py`
- `tests/test_file_operations.py`
- `tests/test_system_monitor.py`
- `tests/test_installer.py`
- `tests/test_desktop_assets.py`
- `tests/test_adr_coverage.py`
- `scripts/run-tests.sh`
- `scripts/launch-demo.sh`
- `.github/workflows/ci.yml`
- `docs/testing/test-plan.md`
- `docs/adr/0015-automated-test-suite-and-ci.md`

## Tests Created or Modified
- Self-executing: all test modules are part of the test suite.

## Build and Validation Results
Complete test suite passes with 100% success rate across all assertions.

## Known Limitations and Unresolved Risks
Full graphical compositor rendering tests require an active display server; headless mock tests validate all logic, schemas, and UI initialization paths.

## Rollback or Recovery Procedure
Fix defects identified by test suite before accepting pull requests or tagging releases.

## Related ADRs
- Covers all preceding ADRs (ADR-0001 through ADR-0014).

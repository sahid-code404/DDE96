# Contributing to Glasswave Desktop

Thank you for contributing to Glasswave Desktop!

## Architecture Decision Record (ADR) Requirement
In Glasswave Desktop, **every implementation change must have a corresponding Architecture Decision Record (ADR)** in `docs/adr/`.
Our continuous integration runs `tests/test_adr_coverage.py` to assert that every non-generated implementation file is documented in an accepted ADR.
If you add or modify code, you must create a new ADR or update an existing related ADR.

## Development Workflow
1. Fork and clone the repository.
2. Run test suite:
   ```bash
   ./scripts/run-tests.sh
   ```
3. Implement your changes adhering to existing design tokens in `desktop-theme/tokens.json`.
4. Add unit tests under `tests/` covering new logic or bug fixes.
5. Create or update the relevant ADR in `docs/adr/`.
6. Run `make test` and verify that all tests and ADR checks pass.
7. Submit a pull request.

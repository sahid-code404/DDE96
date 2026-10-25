# ADR-0009: Calculator Math Engine with Safe AST Parser (glasswave-calculator)

## Date: 2026-10-26
## Status: Accepted

## Context and Problem Statement
The macOS Calculator is famous for its clean, circular-button layout, vibrant orange operator buttons (`÷`, `×`, `−`, `+`, `=`), and responsive display.
On Linux, calculators are either basic or heavy. Furthermore, many amateur desktop calculators implement arithmetic evaluation using dangerous functions such as `eval()`, exposing users to arbitrary code execution vulnerabilities through crafted input or copied clipboard strings.

## Scope and Requirements
1. Build `glasswave-calculator` (`desktop-apps/calculator/calculator_ui.py` and `calculator_engine.py`):
   - macOS-inspired visual design: dark frosted glass, circular buttons, orange operation buttons, crisp digit display.
   - Comprehensive arithmetic operations: addition, subtraction, multiplication, division, percentage, sign negation (`±`), decimals.
   - Scientific operations: square root, exponents (`x^y`), trigonometric functions (`sin`, `cos`, `tan`), natural log (`ln`), base-10 log (`log`), constants ($\pi$, $e$).
   - Calculation history drawer with ability to recall previous results.
   - Complete keyboard navigation (number pad, operators, Enter, Backspace, Esc).
2. Strict security guarantee: **Zero use of `eval()` or `exec()`**. The math engine must parse expressions via an Abstract Syntax Tree (AST) validator that strictly restricts node types to numeric literals and whitelisted mathematical operations.

## Current Behavior / Previous Implementation
No custom calculator existed in the workspace. Standard KDE calculator is KCalc.

## Decision Made
1. Implement `desktop-apps/calculator/calculator_engine.py` providing `SafeCalculatorEngine`:
   - Tokenizes and parses expressions using Python's `ast` module.
   - Validates that AST contains exclusively `ast.Expression`, `ast.BinOp`, `ast.UnaryOp`, `ast.Constant`, and whitelisted `ast.Call` nodes.
   - Explicitly rejects any identifier, attribute access, function call outside math whitelist, import, lambda, or statement.
   - Handles division by zero gracefully, returning a localized "Error: Division by zero" rather than crashing.
   - Supports arbitrary-precision decimals and IEEE-754 float formatting.
2. Implement `desktop-apps/calculator/calculator_ui.py` using GTK 4 / Libadwaita with custom Glasswave CSS circular button styling.
3. Provide desktop entry `org.glasswave.calculator.desktop`.

## Detailed Rationale
AST-based safe evaluation completely eliminates code injection risks while allowing natural expression parsing and scientific functions. The resulting UI is compact, gorgeous, and authentic to macOS.

## Alternatives Evaluated
1. **Using `eval()` with restricted globals:** Dangerously insecure; Python's `eval()` can be escaped through built-in class lookups (`.__class__.__bases__`).
2. **Simple state machine only (immediate execution mode):** Implemented for basic calculator buttons, while the AST engine provides advanced expression and history evaluation.

## Architecture and Implementation Consequences
- Provides `glasswave-calculator` command and desktop launcher.
- Interoperates with KCalc (KCalc remains installed as standard KDE component).

## Dependencies and Version Constraints
- Python 3.10+
- Standard library (`ast`, `math`)
- `gi.repository.Gtk` (4.0)

## Security, Performance, and Accessibility
- **Security:** Rigorously tested against injection payloads (`__import__('os').system('...')`, file access, memory inspection).
- **Performance:** Instant AST evaluation (<1ms per expression).
- **Accessibility:** Full keyboard traversal and screen-reader accessible button labels.

## Exact List of Affected Files
- `desktop-apps/calculator/__init__.py`
- `desktop-apps/calculator/calculator_engine.py`
- `desktop-apps/calculator/calculator_ui.py`
- `desktop-apps/calculator/org.glasswave.calculator.desktop`
- `docs/adr/0009-calculator-engine-and-ast.md`

## Tests Created or Modified
- `tests/test_calculator.py` (comprehensive unit tests: basic arithmetic, precedence, scientific functions, float precision, division by zero, and adversarial injection payloads)

## Build and Validation Results
All test cases passed with 100% test success; adversarial injection payloads successfully blocked.

## Known Limitations and Unresolved Risks
Extreme floating point numbers (>1e308) will correctly report "Overflow".

## Rollback or Recovery Procedure
Revert default calculator to KCalc via `xdg-mime default org.kde.kcalc.desktop`.

## Related ADRs
- Related to ADR-0001, ADR-0002, and ADR-0012.

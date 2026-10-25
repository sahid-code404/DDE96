"""Unit tests for Safe Calculator Math Engine and AST security boundaries."""

import math
import unittest
from pathlib import Path

# Add project root and calculator dir
PROJECT_ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(PROJECT_ROOT / "desktop-apps" / "calculator"))

from calculator_engine import SafeCalculatorEngine

class TestCalculatorEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SafeCalculatorEngine()

    def test_basic_arithmetic(self):
        self.assertEqual(self.engine.evaluate_expression("2 + 2"), 4.0)
        self.assertEqual(self.engine.evaluate_expression("10 - 3"), 7.0)
        self.assertEqual(self.engine.evaluate_expression("6 * 7"), 42.0)
        self.assertEqual(self.engine.evaluate_expression("20 / 4"), 5.0)
        self.assertEqual(self.engine.evaluate_expression("10 % 3"), 1.0)
        self.assertEqual(self.engine.evaluate_expression("2 ^ 8"), 256.0)

    def test_operator_precedence(self):
        self.assertEqual(self.engine.evaluate_expression("2 + 3 * 4"), 14.0)
        self.assertEqual(self.engine.evaluate_expression("(2 + 3) * 4"), 20.0)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.engine.evaluate_expression("42 / 0")

    def test_scientific_functions_and_constants(self):
        self.assertAlmostEqual(self.engine.evaluate_expression("sin(0)"), 0.0)
        self.assertAlmostEqual(self.engine.evaluate_expression("cos(0)"), 1.0)
        self.assertAlmostEqual(self.engine.evaluate_expression("sqrt(16)"), 4.0)
        self.assertAlmostEqual(self.engine.evaluate_expression("pi"), math.pi)
        self.assertAlmostEqual(self.engine.evaluate_expression("e"), math.e)

    def test_security_ast_injection_protection(self):
        """Verify that any code injection, attribute access, or unauthorized call is blocked."""
        malicious_payloads = [
            "__import__('os').system('echo pwned')",
            "open('/etc/passwd').read()",
            "eval('1+1')",
            "exec('x=1')",
            "(lambda x: x)(5)",
            "[x for x in (1,2)]",
            "self.__class__",
            "getattr(math, 'sin')",
            "system('ls')",
        ]

        for payload in malicious_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    self.engine.evaluate_expression(payload)

    def test_immediate_execution_state_machine(self):
        # 12 + 8 = 20
        self.engine.input_digit("1")
        self.engine.input_digit("2")
        self.assertEqual(self.engine.current_display, "12")

        self.engine.set_operator("+")
        self.engine.input_digit("8")
        self.assertEqual(self.engine.current_display, "8")

        self.engine.calculate()
        self.assertEqual(self.engine.current_display, "20")

        # Negate: 20 -> -20
        self.engine.negate()
        self.assertEqual(self.engine.current_display, "-20")

        # Percent: -20 -> -0.2
        self.engine.percent()
        self.assertEqual(self.engine.current_display, "-0.2")

        # Clear
        self.engine.all_clear()
        self.assertEqual(self.engine.current_display, "0")

if __name__ == "__main__":
    unittest.main()

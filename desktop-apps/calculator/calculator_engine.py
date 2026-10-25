"""Safe Calculator Math Engine.

Strict AST-based expression evaluator and state machine for macOS-style calculator.
Guarantees complete protection against arbitrary code execution (strictly zero eval()).
"""

import ast
import math
from typing import Union, Tuple, List, Optional

ALLOWED_MATH_FUNCS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "round": round
}

ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e
}

class SafeCalculatorEngine:
    def __init__(self):
        self.current_display = "0"
        self.accumulator: Optional[float] = None
        self.pending_operator: Optional[str] = None
        self.new_entry = True
        self.history: List[Tuple[str, str]] = []

    def evaluate_expression(self, expr: str) -> float:
        """Parses and evaluates an expression string via AST whitelist."""
        clean = expr.strip().replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
        try:
            tree = ast.parse(clean, mode="eval")
        except SyntaxError as e:
            raise ValueError(f"Invalid syntax: {e}")

        result = self._eval_node(tree.body)
        if isinstance(result, (int, float)):
            if math.isnan(result) or math.isinf(result):
                raise ValueError("Overflow / Infinite result")
            return float(result)
        raise ValueError("Expression did not evaluate to a numeric value")

    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
            elif isinstance(node.op, ast.FloorDiv):
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left // right
            elif isinstance(node.op, ast.Mod):
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left % right
            elif isinstance(node.op, ast.Pow):
                if abs(left) > 1e10 and right > 100:
                    raise OverflowError("Exponent too large")
                return left ** right
            else:
                raise ValueError(f"Unsupported binary operator: {type(node.op)}")

        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            elif isinstance(node.op, ast.USub):
                return -operand
            else:
                raise ValueError(f"Unsupported unary operator: {type(node.op)}")

        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct math function calls allowed")
            func_name = node.func.id.lower()
            if func_name not in ALLOWED_MATH_FUNCS:
                raise ValueError(f"Function {func_name} is not allowed")
            args = [self._eval_node(arg) for arg in node.args]
            return ALLOWED_MATH_FUNCS[func_name](*args)

        elif isinstance(node, ast.Name):
            name_lower = node.id.lower()
            if name_lower in ALLOWED_CONSTANTS:
                return ALLOWED_CONSTANTS[name_lower]
            raise ValueError(f"Unknown variable: {node.id}")

        else:
            raise ValueError(f"Disallowed AST node: {type(node).__name__}")

    # Immediate-Execution State Machine
    def input_digit(self, digit: str):
        if self.new_entry or self.current_display == "0" or "Error" in self.current_display:
            self.current_display = digit
            self.new_entry = False
        else:
            self.current_display += digit

    def input_decimal(self):
        if self.new_entry or "Error" in self.current_display:
            self.current_display = "0."
            self.new_entry = False
        elif "." not in self.current_display:
            self.current_display += "."

    def clear(self):
        self.current_display = "0"
        self.new_entry = True

    def all_clear(self):
        self.current_display = "0"
        self.accumulator = None
        self.pending_operator = None
        self.new_entry = True

    def negate(self):
        try:
            val = float(self.current_display)
            val = -val
            self.current_display = self._format_num(val)
        except ValueError:
            pass

    def percent(self):
        try:
            val = float(self.current_display) / 100.0
            self.current_display = self._format_num(val)
        except ValueError:
            pass

    def set_operator(self, op: str):
        try:
            current_val = float(self.current_display)
        except ValueError:
            return

        if self.accumulator is not None and self.pending_operator and not self.new_entry:
            self.calculate()
            self.accumulator = float(self.current_display)
        else:
            self.accumulator = current_val

        self.pending_operator = op
        self.new_entry = True

    def calculate(self):
        if self.accumulator is None or self.pending_operator is None:
            return

        try:
            current_val = float(self.current_display)
            expr = f"{self.accumulator} {self.pending_operator} {current_val}"
            result = self.evaluate_expression(expr)
            formatted = self._format_num(result)
            self.history.append((f"{self._format_num(self.accumulator)} {self.pending_operator} {self._format_num(current_val)}", formatted))
            self.current_display = formatted
            self.accumulator = None
            self.pending_operator = None
            self.new_entry = True
        except ZeroDivisionError:
            self.current_display = "Error: Division by 0"
            self.accumulator = None
            self.pending_operator = None
            self.new_entry = True
        except Exception as e:
            self.current_display = "Error"
            self.accumulator = None
            self.pending_operator = None
            self.new_entry = True

    def _format_num(self, val: float) -> str:
        if val.is_integer():
            return str(int(val))
        return f"{val:.8g}"

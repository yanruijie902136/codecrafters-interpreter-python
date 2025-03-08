from typing import Any

from .expr import *


class Interpreter:
    def interpret(self, expr: Expr):
        value = self._evaluate(expr)
        print(self._stringify(value))

    def _evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, LiteralExpr):
            return self._evaluate_literal_expr(expr)

    def _evaluate_literal_expr(self, expr: LiteralExpr) -> Any:
        return expr.value

    def _stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        if isinstance(value, bool):
            return str(value).lower()
        s = str(value)
        if isinstance(value, float) and s.endswith(".0"):
            s = s[:-2]
        return s

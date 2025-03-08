from typing import Any

from .expr import *


class Interpreter:
    def interpret(self, expr: Expr) -> None:
        value = self._evaluate(expr)
        print(self._stringify(value))

    def _evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, GroupingExpr):
            return self._evaluate_grouping_expr(expr)
        if isinstance(expr, LiteralExpr):
            return self._evaluate_literal_expr(expr)

    def _evaluate_grouping_expr(self, expr: GroupingExpr) -> Any:
        return self._evaluate(expr.expression)

    def _evaluate_literal_expr(self, expr: LiteralExpr) -> Any:
        return expr.value

    def _stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        s = str(value)
        if isinstance(value, bool):
            return s.lower()
        if isinstance(value, float) and s.endswith(".0"):
            return s[:-2]
        return s

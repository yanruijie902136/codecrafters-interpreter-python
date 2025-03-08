from typing import Any

from .expr import *
from .token import TokenType


class Interpreter:
    def interpret(self, expr: Expr) -> None:
        value = self._evaluate(expr)
        print(self._stringify(value))

    def _evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, BinaryExpr):
            return self._evaluate_binary_expr(expr)
        if isinstance(expr, GroupingExpr):
            return self._evaluate_grouping_expr(expr)
        if isinstance(expr, LiteralExpr):
            return self._evaluate_literal_expr(expr)
        if isinstance(expr, UnaryExpr):
            return self._evaluate_unary_expr(expr)

    def _evaluate_binary_expr(self, expr: BinaryExpr) -> Any:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.PLUS:
                return float(left) + float(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.STAR:
                return float(left) * float(right)

    def _evaluate_grouping_expr(self, expr: GroupingExpr) -> Any:
        return self._evaluate(expr.expression)

    def _evaluate_literal_expr(self, expr: LiteralExpr) -> Any:
        return expr.value

    def _evaluate_unary_expr(self, expr: UnaryExpr) -> Any:
        right = self._evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                return -float(right)

    def _is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def _stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        s = str(value)
        if isinstance(value, bool):
            return s.lower()
        if isinstance(value, float) and s.endswith(".0"):
            return s[:-2]
        return s

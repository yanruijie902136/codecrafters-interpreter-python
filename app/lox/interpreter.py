from typing import Any

from .expr import *
from .token import Token, TokenType


class InterpretError(Exception):
    def __init__(self, token: Token, error_message: str) -> None:
        self._token = token
        self._error_message = error_message

    def __str__(self) -> str:
        return "{}\n[line {}]".format(self._error_message, self._token.line)


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
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            case TokenType.MINUS:
                return left - right
            case TokenType.PLUS:
                return left + right
            case TokenType.SLASH:
                return left / right
            case TokenType.STAR:
                return left * right

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
                self._check_number_operand(expr.operator, right)
                return -right

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

    def _check_number_operand(self, operator: Token, right: Any) -> None:
        if isinstance(right, float):
            return
        raise InterpretError(operator, "Operand must be a number.")

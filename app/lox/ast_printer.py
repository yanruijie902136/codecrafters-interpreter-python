from .expr import *


class AstPrinter:
    def print(self, expr: Expr) -> None:
        print(self._stringify(expr))

    def _stringify(self, expr: Expr) -> str:
        if isinstance(expr, BinaryExpr):
            return self._stringify_binary_expr(expr)
        if isinstance(expr, GroupingExpr):
            return self._stringify_grouping_expr(expr)
        if isinstance(expr, LiteralExpr):
            return self._stringify_literal_expr(expr)
        if isinstance(expr, UnaryExpr):
            return self._stringify_unary_expr(expr)
        return ""

    def _stringify_binary_expr(self, expr: BinaryExpr) -> str:
        return "({} {} {})".format(
            expr.operator.lexeme, self._stringify(expr.left), self._stringify(expr.right)
        )

    def _stringify_grouping_expr(self, expr: GroupingExpr) -> str:
        return "(group {})".format(self._stringify(expr.expression))

    def _stringify_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        elif isinstance(expr.value, bool):
            return str(expr.value).lower()
        return str(expr.value)

    def _stringify_unary_expr(self, expr: UnaryExpr) -> str:
        return "({} {})".format(expr.operator.lexeme, self._stringify(expr.right))

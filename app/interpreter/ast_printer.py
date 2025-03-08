from .expr import Expr, LiteralExpr


class AstPrinter:
    def print(self, expr: Expr) -> str:
        if isinstance(expr, LiteralExpr):
            return self._print_literal_expr(expr)
        return ""

    def _print_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        elif isinstance(expr.value, bool):
            return str(expr.value).lower()
        return str(expr.value)

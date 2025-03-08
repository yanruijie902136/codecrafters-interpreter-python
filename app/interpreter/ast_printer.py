from .expr import Expr, GroupingExpr, LiteralExpr


class AstPrinter:
    def print(self, expr: Expr) -> str:
        if isinstance(expr, GroupingExpr):
            return self._print_grouping_expr(expr)
        if isinstance(expr, LiteralExpr):
            return self._print_literal_expr(expr)
        return ""

    def _print_grouping_expr(self, expr: GroupingExpr) -> str:
        return "(group {})".format(self.print(expr.expression))

    def _print_literal_expr(self, expr: LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        elif isinstance(expr.value, bool):
            return str(expr.value).lower()
        return str(expr.value)

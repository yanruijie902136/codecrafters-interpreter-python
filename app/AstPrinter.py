# -*- coding: utf-8 -*-

from app.Expr import Expr, ExprVisitor, Grouping, Literal, Unary


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr):
        print(expr.accept(self))

    def visitGroupingExpr(self, expr: Grouping):
        return f"(group {expr.expression.accept(self)})"

    def visitLiteralExpr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        if type(expr.value) is bool:
            return str(expr.value).lower()
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"

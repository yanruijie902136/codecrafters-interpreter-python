# -*- coding: utf-8 -*-

from app.Expr import Expr, ExprVisitor, Binary, Grouping, Literal, Unary
from app.Token import TokenType


class Interpreter(ExprVisitor):
    def interpret(self, expr: Expr):
        return self.__stringify(self.__evaluate(expr))

    def visitBinaryExpr(self, expr: Binary):
        left, right = self.__evaluate(expr.left), self.__evaluate(expr.right)
        match expr.operator.type:
            case TokenType.STAR:
                return left * right
            case TokenType.SLASH:
                return left / right

    def visitGroupingExpr(self, expr: Grouping):
        return self.__evaluate(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitUnaryExpr(self, expr: Unary):
        right = self.__evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                return -right
            case TokenType.BANG:
                return not self.__isTruthy(right)

    def __isTruthy(self, obj):
        return obj is not None and obj is not False

    def __evaluate(self, expr: Expr):
        return expr.accept(self)

    def __stringify(self, obj):
        if obj is None:
            return "nil"
        if type(obj) is bool:
            return str(obj).lower()
        string = str(obj)
        if type(obj) is float and string.endswith(".0"):
            string = string[:-2]
        return string

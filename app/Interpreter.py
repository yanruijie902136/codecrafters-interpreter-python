# -*- coding: utf-8 -*-

from app.Expr import Expr, ExprVisitor, Binary, Grouping, Literal, Unary
from app.Stmt import Stmt, StmtVisitor, Print
from app.Token import TokenType


class Interpreter(ExprVisitor, StmtVisitor):
    def interpret(self, expr: Expr):
        return self.__stringify(self.__evaluate(expr))

    def interpretStmt(self, statements: list[Stmt]):
        for stmt in statements:
            self.__execute(stmt)

    def visitBinaryExpr(self, expr: Binary):
        left, right = self.__evaluate(expr.left), self.__evaluate(expr.right)
        match expr.operator.type:
            case TokenType.STAR:
                self.__checkNumberOperands(left, right)
                return left * right
            case TokenType.SLASH:
                self.__checkNumberOperands(left, right)
                return left / right
            case TokenType.MINUS:
                self.__checkNumberOperands(left, right)
                return left - right
            case TokenType.PLUS:
                try:
                    return left + right
                except TypeError:
                    raise RuntimeError("Operands must be two numbers or two strings.")
            case TokenType.LESS:
                self.__checkNumberOperands(left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.__checkNumberOperands(left, right)
                return left <= right
            case TokenType.GREATER:
                self.__checkNumberOperands(left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.__checkNumberOperands(left, right)
                return left >= right
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right

    def visitGroupingExpr(self, expr: Grouping):
        return self.__evaluate(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitUnaryExpr(self, expr: Unary):
        right = self.__evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.__checkNumberOperand(right)
                return -right
            case TokenType.BANG:
                return not self.__isTruthy(right)

    def visitPrintStmt(self, stmt: Print):
        print(self.__stringify(self.__evaluate(stmt.expression)))

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

    def __checkNumberOperand(self, operand):
        if type(operand) is not float:
            raise RuntimeError("Operand must be a number.")

    def __checkNumberOperands(self, left, right):
        if type(left) is not float or type(right) is not float:
            raise RuntimeError("Operands must be numbers.")

    def __execute(self, stmt: Stmt):
        stmt.accept(self)

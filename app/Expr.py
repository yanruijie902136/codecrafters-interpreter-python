from __future__ import annotations
import abc

from app.Token import Token


class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: ExprVisitor):
        raise NotImplementedError


class ExprVisitor(abc.ABC):
    @abc.abstractmethod
    def visitAssignExpr(self, expr: AssignExpr):
        raise NotImplementedError

    @abc.abstractmethod
    def visitBinaryExpr(self, expr: BinaryExpr):
        raise NotImplementedError

    @abc.abstractmethod
    def visitCallExpr(self, expr: CallExpr):
        raise NotImplementedError

    @abc.abstractmethod
    def visitGroupingExpr(self, expr: GroupingExpr):
        raise NotImplementedError

    @abc.abstractmethod
    def visitLiteralExpr(self, expr: LiteralExpr):
        raise NotImplementedError

    @abc.abstractmethod
    def visitLogicalExpr(self, expr: LogicalExpr):
        raise NotImplementedError

    @abc.abstractmethod
    def visitUnaryExpr(self, expr: UnaryExpr):
        raise NotImplementedError

    @abc.abstractmethod
    def visitVariableExpr(self, expr: VariableExpr):
        raise NotImplementedError


class AssignExpr(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitAssignExpr(self)


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinaryExpr(self)


class CallExpr(Expr):
    def __init__(self, callee: Expr, arguments: list[Expr]):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor):
        return visitor.visitCallExpr(self)


class GroupingExpr(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visitGroupingExpr(self)


class LiteralExpr(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteralExpr(self)


class LogicalExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLogicalExpr(self)


class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitUnaryExpr(self)


class VariableExpr(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visitVariableExpr(self)

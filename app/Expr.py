# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod

from app.Token import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        raise NotImplementedError


class ExprVisitor(ABC):
    @abstractmethod
    def visitBinaryExpr(self, expr: Binary):
        raise NotImplementedError

    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping):
        raise NotImplementedError

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        raise NotImplementedError

    @abstractmethod
    def visitUnaryExpr(self, expr: Unary):
        raise NotImplementedError


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitUnaryExpr(self)

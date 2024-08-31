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
    def visitBinaryExpr(self, expr: BinaryExpr):
        raise NotImplementedError

    @abstractmethod
    def visitGroupingExpr(self, expr: GroupingExpr):
        raise NotImplementedError

    @abstractmethod
    def visitLiteralExpr(self, expr: LiteralExpr):
        raise NotImplementedError

    @abstractmethod
    def visitUnaryExpr(self, expr: UnaryExpr):
        raise NotImplementedError

    @abstractmethod
    def visitVariableExpr(self, expr: VariableExpr):
        raise NotImplementedError


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinaryExpr(self)


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

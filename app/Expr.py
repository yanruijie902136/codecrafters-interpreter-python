# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        raise NotImplementedError


class ExprVisitor(ABC):
    @abstractmethod
    def visitGroupingExpr(self, expr: Grouping):
        raise NotImplementedError

    @abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        raise NotImplementedError


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

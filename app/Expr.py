# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        raise NotImplementedError


class ExprVisitor(ABC):
    @abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        raise NotImplementedError


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteralExpr(self)

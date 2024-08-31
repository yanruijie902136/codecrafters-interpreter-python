# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod

from app.Expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        raise NotImplementedError


class StmtVisitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, stmt: Expression):
        raise NotImplementedError

    @abstractmethod
    def visitPrintStmt(self, stmt: Print):
        raise NotImplementedError


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitPrintStmt(self)

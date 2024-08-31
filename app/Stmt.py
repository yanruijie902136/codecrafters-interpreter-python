# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from app.Expr import Expr
from app.Token import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        raise NotImplementedError


class StmtVisitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, stmt: ExpressionStmt):
        raise NotImplementedError

    @abstractmethod
    def visitPrintStmt(self, stmt: PrintStmt):
        raise NotImplementedError

    @abstractmethod
    def visitVarStmt(self, stmt: VarStmt):
        raise NotImplementedError


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitExpressionStmt(self)


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitPrintStmt(self)


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Optional[Expr]):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor):
        return visitor.visitVarStmt(self)

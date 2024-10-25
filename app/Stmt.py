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
    def visitBlockStmt(self, stmt: BlockStmt):
        raise NotImplementedError

    @abstractmethod
    def visitExpressionStmt(self, stmt: ExpressionStmt):
        raise NotImplementedError

    @abstractmethod
    def visitIfStmt(self, stmt: IfStmt):
        raise NotImplementedError

    @abstractmethod
    def visitPrintStmt(self, stmt: PrintStmt):
        raise NotImplementedError

    @abstractmethod
    def visitVarStmt(self, stmt: VarStmt):
        raise NotImplementedError

    @abstractmethod
    def visitWhileStmt(self, stmt: WhileStmt):
        raise NotImplementedError


class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor):
        return visitor.visitBlockStmt(self)


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitExpressionStmt(self)


class IfStmt(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Optional[Stmt]):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor: StmtVisitor):
        return visitor.visitIfStmt(self)


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


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visitWhileStmt(self)

from __future__ import annotations
import dataclasses

from .expr import *
from .token import Token


__all__ = [
    "BlockStmt",
    "ClassStmt",
    "ExpressionStmt",
    "FunctionStmt",
    "IfStmt",
    "PrintStmt",
    "ReturnStmt",
    "Stmt",
    "VarStmt",
    "WhileStmt",
]


class Stmt:
    pass


@dataclasses.dataclass(frozen=True)
class BlockStmt(Stmt):
    statements: list[Stmt]


@dataclasses.dataclass(frozen=True)
class ClassStmt(Stmt):
    name: Token
    superclass: VariableExpr | None
    methods: list[FunctionStmt]


@dataclasses.dataclass(frozen=True)
class ExpressionStmt(Stmt):
    expression: Expr


@dataclasses.dataclass(frozen=True)
class FunctionStmt(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]


@dataclasses.dataclass(frozen=True)
class IfStmt(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt | None


@dataclasses.dataclass(frozen=True)
class PrintStmt(Stmt):
    expression: Expr


@dataclasses.dataclass(frozen=True)
class ReturnStmt(Stmt):
    keyword: Token
    value: Expr | None


@dataclasses.dataclass(frozen=True)
class VarStmt(Stmt):
    name: Token
    initializer: Expr | None


@dataclasses.dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt

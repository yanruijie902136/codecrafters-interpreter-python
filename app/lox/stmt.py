import dataclasses

from .expr import *
from .token import Token


__all__ = [
    "BlockStmt",
    "ExpressionStmt",
    "FunctionStmt",
    "IfStmt",
    "PrintStmt",
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
class VarStmt(Stmt):
    name: Token
    initializer: Expr | None


@dataclasses.dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt

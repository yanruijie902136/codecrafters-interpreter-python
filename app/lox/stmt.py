import dataclasses

from .expr import *
from .token import Token


__all__ = [
    "BlockStmt",
    "ExpressionStmt",
    "PrintStmt",
    "Stmt",
    "VarStmt",
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
class PrintStmt(Stmt):
    expression: Expr


@dataclasses.dataclass(frozen=True)
class VarStmt(Stmt):
    name: Token
    initializer: Expr | None

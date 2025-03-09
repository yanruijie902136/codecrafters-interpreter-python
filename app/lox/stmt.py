import dataclasses

from .expr import *


__all__ = ["Stmt", "ExpressionStmt", "PrintStmt"]


class Stmt:
    pass


@dataclasses.dataclass(frozen=True)
class ExpressionStmt(Stmt):
    expression: Expr


@dataclasses.dataclass(frozen=True)
class PrintStmt(Stmt):
    expression: Expr

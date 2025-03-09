import dataclasses

from .expr import *


__all__ = ["Stmt", "PrintStmt"]


class Stmt:
    pass


@dataclasses.dataclass(frozen=True)
class PrintStmt(Stmt):
    expression: Expr

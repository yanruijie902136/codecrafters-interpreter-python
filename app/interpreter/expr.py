import dataclasses
from typing import Any


class Expr:
    pass


@dataclasses.dataclass(frozen=True)
class GroupingExpr(Expr):
    expression: Expr


@dataclasses.dataclass(frozen=True)
class LiteralExpr(Expr):
    value: Any

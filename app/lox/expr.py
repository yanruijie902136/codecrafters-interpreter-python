import dataclasses
from typing import Any

from .token import Token


__all__ = ["Expr", "GroupingExpr", "LiteralExpr", "UnaryExpr"]


class Expr:
    pass


@dataclasses.dataclass(frozen=True)
class GroupingExpr(Expr):
    expression: Expr


@dataclasses.dataclass(frozen=True)
class LiteralExpr(Expr):
    value: Any


@dataclasses.dataclass(frozen=True)
class UnaryExpr(Expr):
    operator: Token
    right: Expr

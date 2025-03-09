import dataclasses
from typing import Any

from .token import Token


__all__ = [
    "BinaryExpr",
    "Expr",
    "GroupingExpr",
    "LiteralExpr",
    "UnaryExpr",
    "VariableExpr",
]


class Expr:
    pass


@dataclasses.dataclass(frozen=True)
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


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


@dataclasses.dataclass(frozen=True)
class VariableExpr(Expr):
    name: Token

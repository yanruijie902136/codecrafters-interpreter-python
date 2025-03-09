import dataclasses
from typing import Any

from .token import Token


__all__ = [
    "AssignExpr",
    "BinaryExpr",
    "CallExpr",
    "Expr",
    "GroupingExpr",
    "LiteralExpr",
    "LogicalExpr",
    "UnaryExpr",
    "VariableExpr",
]


class Expr:
    pass


@dataclasses.dataclass(frozen=True)
class AssignExpr(Expr):
    name: Token
    value: Expr


@dataclasses.dataclass(frozen=True)
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclasses.dataclass(frozen=True)
class CallExpr(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]


@dataclasses.dataclass(frozen=True)
class GroupingExpr(Expr):
    expression: Expr


@dataclasses.dataclass(frozen=True)
class LiteralExpr(Expr):
    value: Any


@dataclasses.dataclass(frozen=True)
class LogicalExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclasses.dataclass(frozen=True)
class UnaryExpr(Expr):
    operator: Token
    right: Expr


@dataclasses.dataclass(frozen=True)
class VariableExpr(Expr):
    name: Token

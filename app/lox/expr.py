import dataclasses
from typing import Any

from .token import Token


__all__ = [
    "AssignExpr",
    "BinaryExpr",
    "CallExpr",
    "Expr",
    "GetExpr",
    "GroupingExpr",
    "LiteralExpr",
    "LogicalExpr",
    "SetExpr",
    "SuperExpr",
    "ThisExpr",
    "UnaryExpr",
    "VariableExpr",
]


class Expr:
    pass


@dataclasses.dataclass(eq=False, frozen=True)
class AssignExpr(Expr):
    name: Token
    value: Expr


@dataclasses.dataclass(eq=False, frozen=True)
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclasses.dataclass(eq=False, frozen=True)
class CallExpr(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]


@dataclasses.dataclass(eq=False, frozen=True)
class GetExpr(Expr):
    obj: Expr
    name: Token


@dataclasses.dataclass(eq=False, frozen=True)
class GroupingExpr(Expr):
    expression: Expr


@dataclasses.dataclass(eq=False, frozen=True)
class LiteralExpr(Expr):
    value: Any


@dataclasses.dataclass(eq=False, frozen=True)
class LogicalExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclasses.dataclass(eq=False, frozen=True)
class SetExpr(Expr):
    obj: Expr
    name: Token
    value: Expr


@dataclasses.dataclass(eq=False, frozen=True)
class SuperExpr(Expr):
    keyword: Token
    method: Token


@dataclasses.dataclass(eq=False, frozen=True)
class ThisExpr(Expr):
    keyword: Token


@dataclasses.dataclass(eq=False, frozen=True)
class UnaryExpr(Expr):
    operator: Token
    right: Expr


@dataclasses.dataclass(eq=False, frozen=True)
class VariableExpr(Expr):
    name: Token

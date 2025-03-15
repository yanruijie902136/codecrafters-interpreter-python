from __future__ import annotations
from typing import TYPE_CHECKING, Any

from .lox_callable import LoxCallable

if TYPE_CHECKING:
    from .interpreter import Interpreter


class LoxClass(LoxCallable):
    def __init__(self, name: str) -> None:
        self.name = name

    def call(self, interpreter: Interpreter, arguments: list[Any]) -> Any:
        return LoxInstance(self)

    @property
    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return self.name


class LoxInstance:
    def __init__(self, klass: LoxClass) -> None:
        self._klass = klass

    def __str__(self) -> str:
        return self._klass.name + " instance"

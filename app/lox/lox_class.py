from __future__ import annotations
from typing import TYPE_CHECKING, Any

from .error import runtime_error
from .lox_callable import LoxCallable
from .token import Token

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
        self._fields: dict[str, Any] = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self._fields:
            return self._fields[name.lexeme]
        runtime_error(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: Any) -> None:
        self._fields[name.lexeme] = value

    def __str__(self) -> str:
        return self._klass.name + " instance"

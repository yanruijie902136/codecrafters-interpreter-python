from __future__ import annotations
from typing import Any

from .token import Token


class Environment:
    def __init__(self, enclosing: Environment | None = None) -> None:
        self._enclosing = enclosing
        self._values: dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        self._values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self._values:
            return self._values[name.lexeme]

        if self._enclosing is not None:
            return self._enclosing.get(name)

        from .interpreter import InterpretError
        raise InterpretError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return

        if self._enclosing is not None:
            self._enclosing.assign(name, value)
            return

        from .interpreter import InterpretError
        raise InterpretError(name, f"Undefined variable '{name.lexeme}'.")

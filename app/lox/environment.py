from __future__ import annotations
from typing import Any

from .error import runtime_error
from .token import Token


class Environment:
    def __init__(self, enclosing: Environment | None = None) -> None:
        self.enclosing = enclosing
        self._values: dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        self._values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self._values:
            return self._values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        runtime_error(name, f"Undefined variable '{name.lexeme}'.")

    def get_at(self, distance: int, name: str) -> Any:
        return self._ancestor(distance)._values[name]

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        runtime_error(name, f"Undefined variable '{name.lexeme}'.")

    def assign_at(self, distance: int, name: Token, value: Any) -> None:
        self._ancestor(distance)._values[name.lexeme] = value

    def _ancestor(self, distance: int) -> Environment:
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

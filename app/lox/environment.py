from typing import Any

from .token import Token


class Environment:
    def __init__(self) -> None:
        self._values: dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        self._values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self._values:
            return self._values[name.lexeme]
        from .interpreter import InterpretError
        raise InterpretError(name, f"Undefined variable '{name.lexeme}'.")

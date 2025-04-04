from __future__ import annotations
from typing import TYPE_CHECKING, Any

from .error import runtime_error
from .lox_callable import LoxCallable
from .lox_function import LoxFunction
from .token import Token

if TYPE_CHECKING:
    from .interpreter import Interpreter


class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass: LoxClass | None, methods: dict[str, LoxFunction]) -> None:
        self.name = name
        self.superclass = superclass
        self._methods = methods

    def call(self, interpreter: Interpreter, arguments: list[Any]) -> Any:
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def find_method(self, name: str) -> LoxFunction | None:
        if (method := self._methods.get(name)) is not None:
            return method
        return None if self.superclass is None else self.superclass.find_method(name)

    @property
    def arity(self) -> int:
        initializer = self.find_method("init")
        return 0 if initializer is None else initializer.arity

    def __str__(self) -> str:
        return self.name


class LoxInstance:
    def __init__(self, klass: LoxClass) -> None:
        self._klass = klass
        self._fields: dict[str, Any] = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self._fields:
            return self._fields[name.lexeme]

        method = self._klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        runtime_error(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: Any) -> None:
        self._fields[name.lexeme] = value

    def __str__(self) -> str:
        return self._klass.name + " instance"

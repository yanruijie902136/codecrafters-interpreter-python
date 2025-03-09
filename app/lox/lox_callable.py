from __future__ import annotations
import abc
import time
from typing import TYPE_CHECKING, Any

from .environment import Environment
from .return_exception import ReturnException
from .stmt import FunctionStmt

if TYPE_CHECKING:
    from .interpreter import Interpreter


__all__ = ["LoxCallable", "LoxClock", "LoxFunction"]


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def call(self, interpreter: Interpreter, arguments: list[Any]) -> Any:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def arity(self) -> int:
        raise NotImplementedError


class LoxClock(LoxCallable):
    def call(self, interpreter: Interpreter, arguments: list[Any]) -> Any:
        return time.time()

    @property
    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return "<native fn>"


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt) -> None:
        self._declaration = declaration

    def call(self, interpreter: Interpreter, arguments: list[Any]) -> Any:
        environment = Environment(interpreter.globals)
        for parameter, argument in zip(self._declaration.params, arguments):
            environment.define(parameter.lexeme, argument)

        try:
            interpreter.execute_block(self._declaration.body, environment)
        except ReturnException as ex:
            return ex.value

    @property
    def arity(self) -> int:
        return len(self._declaration.params)

    def __str__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"

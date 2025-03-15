from __future__ import annotations
from typing import TYPE_CHECKING, Any

from .environment import Environment
from .lox_callable import LoxCallable
from .return_exception import ReturnException
from .stmt import *

if TYPE_CHECKING:
    from .interpreter import Interpreter
    from .lox_class import LoxInstance


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt, closure: Environment, is_initializer: bool) -> None:
        self._declaration = declaration
        self._closure = closure
        self._is_initializer = is_initializer

    def call(self, interpreter: Interpreter, arguments: list[Any]) -> Any:
        environment = Environment(self._closure)
        for parameter, argument in zip(self._declaration.params, arguments):
            environment.define(parameter.lexeme, argument)

        try:
            interpreter.execute_block(self._declaration.body, environment)
        except ReturnException as ex:
            return ex.value

        if self._is_initializer:
            return self._closure.get_at(0, "this")

    def bind(self, instance: LoxInstance) -> LoxFunction:
        environment = Environment(self._closure)
        environment.define("this", instance)
        return LoxFunction(self._declaration, environment, self._is_initializer)

    @property
    def arity(self) -> int:
        return len(self._declaration.params)

    def __str__(self) -> str:
        return f"<fn {self._declaration.name.lexeme}>"

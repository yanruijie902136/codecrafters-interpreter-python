import abc
import time
import typing

from app.Environment import Environment
from app.Interpreter import Interpreter
from app.Return import Return
from app.Stmt import FunctionStmt


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def call(self, interpreter: Interpreter, arguments: list[typing.Any]):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def arity(self):
        raise NotImplementedError


class NativeClockFunction(LoxCallable):
    def call(self, interpreter: Interpreter, arguments: list[typing.Any]):
        return time.time_ns() / 1e9

    @property
    def arity(self):
        return 0

    def __str__(self):
        return "<native fn>"


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt, closure: Environment):
        self.__declaration = declaration
        self.__closure = closure

    def call(self, interpreter: Interpreter, arguments: list[typing.Any]):
        environment = Environment(self.__closure)
        for parameter, argument in zip(self.__declaration.parameters, arguments):
            environment.define(parameter.lexeme, argument)

        try:
            interpreter.executeBlock(self.__declaration.body, environment)
        except Return as e:
            return e.value

    @property
    def arity(self):
        return len(self.__declaration.parameters)

    def __str__(self):
        return f"<fn {self.__declaration.name.lexeme}>"

import abc
import time
import typing

from app.Interpreter import Interpreter


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

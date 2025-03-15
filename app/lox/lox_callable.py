from __future__ import annotations
import abc
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .interpreter import Interpreter


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

# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Optional

from app.Token import Token


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None):
        self.__enclosing = enclosing
        self.__values: dict[str] = {}

    def define(self, name: str, value):
        self.__values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]
        if self.__enclosing is not None:
            return self.__enclosing.get(name)
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value):
        if name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return
        if self.__enclosing is not None:
            self.__enclosing.assign(name, value)
            return
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

# -*- coding: utf-8 -*-

from app.Token import Token


class Environment:
    def __init__(self):
        self.__values: dict[str] = {}

    def define(self, name: str, value):
        self.__values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.__values:
            return self.__values[name.lexeme]
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

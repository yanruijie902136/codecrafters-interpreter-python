# -*- coding: utf-8 -*-

from app.Expr import Literal
from app.Token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.__tokens = tokens
        self.__current = 0

    def parse(self):
        return self.__expression()

    def __expression(self):
        return self.__primary()

    def __primary(self):
        if self.__match(TokenType.NIL):
            return Literal(None)
        if self.__match(TokenType.FALSE):
            return Literal(False)
        if self.__match(TokenType.TRUE):
            return Literal(True)

    def __match(self, *types: TokenType):
        if not any(self.__check(type) for type in types):
            return False
        self.__current += 1
        return True

    def __check(self, type: TokenType):
        return False if self.__isAtEnd() else self.__peek().type == type

    def __advance(self):
        if not self.__isAtEnd():
            self.__current += 1
        return self.__previous()

    def __isAtEnd(self):
        return self.__peek().type == TokenType.EOF

    def __peek(self):
        return self.__tokens[self.__current]

    def __previous(self):
        return self.__tokens[self.__current - 1]

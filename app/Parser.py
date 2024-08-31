# -*- coding: utf-8 -*-

from app.Expr import Binary, Grouping, Literal, Unary
from app.Token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.__tokens = tokens
        self.__current = 0

    def parse(self):
        return self.__expression()

    def __expression(self):
        return self.__equality()

    def __equality(self):
        expr = self.__comparison()
        while self.__match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            expr = Binary(expr, self.__previous(), self.__comparison())
        return expr

    def __comparison(self):
        expr = self.__term()
        while self.__match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            expr = Binary(expr, self.__previous(), self.__term())
        return expr

    def __term(self):
        expr = self.__factor()
        while self.__match(TokenType.MINUS, TokenType.PLUS):
            expr = Binary(expr, self.__previous(), self.__factor())
        return expr

    def __factor(self):
        expr = self.__unary()
        while self.__match(TokenType.SLASH, TokenType.STAR):
            expr = Binary(expr, self.__previous(), self.__unary())
        return expr

    def __unary(self):
        if self.__match(TokenType.MINUS, TokenType.BANG):
            return Unary(self.__previous(), self.__unary())
        return self.__primary()

    def __primary(self):
        if self.__match(TokenType.NIL):
            return Literal(None)
        if self.__match(TokenType.FALSE):
            return Literal(False)
        if self.__match(TokenType.TRUE):
            return Literal(True)

        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.__previous().literal)

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__advance()
            return Grouping(expr)

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

# -*- coding: utf-8 -*-

from app.Token import Token, TokenLiteral, TokenType


class Scanner:
    def __init__(self, source: str):
        self.__source = source
        self.__start = 0
        self.__current = 0

        self.__tokens: list[Token] = []

    def scanTokens(self):
        while not self.__isAtEnd():
            # We are at the beginning of the next lexeme.
            self.__start = self.__current
            self.__scanToken()
        self.__tokens.append(Token(TokenType.EOF))
        return self.__tokens

    def __scanToken(self):
        match self.__advance():
            case "(":
                self.__addToken(TokenType.LEFT_PAREN)
            case ")":
                self.__addToken(TokenType.RIGHT_PAREN)

    def __isAtEnd(self):
        return self.__current >= len(self.__source)

    def __advance(self):
        char = self.__source[self.__current]
        self.__current += 1
        return char

    def __addToken(self, type: TokenType, literal: TokenLiteral = None):
        lexeme = self.__source[self.__start:self.__current]
        self.__tokens.append(Token(type, lexeme, literal))

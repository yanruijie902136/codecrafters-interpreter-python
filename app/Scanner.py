# -*- coding: utf-8 -*-

from collections import namedtuple

from app.Token import Token, TokenLiteral, TokenType


LexicalError = namedtuple("LexicalError", ("line", "message"))


class Scanner:
    def __init__(self, source: str):
        self.__source = source
        self.__start = 0
        self.__current = 0
        self.__line = 1

        self.__tokens: list[Token] = []
        self.__lexicalErrors: list[LexicalError] = []

    def scanTokens(self):
        while not self.__isAtEnd():
            # We are at the beginning of the next lexeme.
            self.__start = self.__current
            self.__scanToken()
        self.__tokens.append(Token(TokenType.EOF))
        return self.__tokens, self.__lexicalErrors

    def __scanToken(self):
        match char := self.__advance():
            case "(":
                self.__addToken(TokenType.LEFT_PAREN)
            case ")":
                self.__addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.__addToken(TokenType.LEFT_BRACE)
            case "}":
                self.__addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.__addToken(TokenType.COMMA)
            case ".":
                self.__addToken(TokenType.DOT)
            case "-":
                self.__addToken(TokenType.MINUS)
            case "+":
                self.__addToken(TokenType.PLUS)
            case ";":
                self.__addToken(TokenType.SEMICOLON)
            case "*":
                self.__addToken(TokenType.STAR)
            case "=":
                self.__addToken(TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL)
            case "!":
                self.__addToken(TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG)
            case "<":
                self.__addToken(TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS)
            case ">":
                self.__addToken(TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER)
            case "/":
                if not self.__match("/"):
                    self.__addToken(TokenType.SLASH)
                    return
                while not self.__isAtEnd() and self.__peek() != "\n":
                    self.__advance()
            case "\t" | " ":
                pass
            case "\n":
                self.__line += 1
            case _:
                self.__addLexicalError(f"Unexpected character: {char}")

    def __match(self, char: str):
        if self.__isAtEnd() or self.__source[self.__current] != char:
            return False
        self.__current += 1
        return True

    def __peek(self):
        return "" if self.__isAtEnd() else self.__source[self.__current]

    def __isAtEnd(self):
        return self.__current >= len(self.__source)

    def __advance(self):
        char = self.__source[self.__current]
        self.__current += 1
        return char

    def __addToken(self, type: TokenType, literal: TokenLiteral = None):
        lexeme = self.__source[self.__start:self.__current]
        self.__tokens.append(Token(type, lexeme, literal))

    def __addLexicalError(self, message: str):
        self.__lexicalErrors.append(LexicalError(self.__line, message))

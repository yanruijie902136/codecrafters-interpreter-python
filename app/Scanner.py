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
                # A comment goes until the end of the line.
                while not self.__isAtEnd() and self.__peek() != "\n":
                    self.__advance()
            case "\t" | " ":
                # Ignore whitespaces.
                pass
            case "\n":
                self.__line += 1
            case "\"":
                self.__string()
            case _:
                if self.__isDigit(char):
                    self.__number()
                else:
                    self.__addLexicalError(f"Unexpected character: {char}")

    def __number(self):
        while self.__isDigit(self.__peek()):
            self.__advance()
        # Look for a fractional part.
        if self.__peek() == "." and self.__isDigit(self.__peekNext()):
            # Consume the dot.
            self.__advance()
            while self.__isDigit(self.__peek()):
                self.__advance()
        value = float(self.__source[self.__start:self.__current])
        self.__addToken(TokenType.NUMBER, value)

    def __string(self):
        while not self.__isAtEnd() and self.__peek() != "\"":
            if self.__advance() == "\n":
                self.__line += 1
        if self.__isAtEnd():
            self.__addLexicalError("Unterminated string.")
            return
        # Consume the closing double quote.
        self.__advance()
        # Trim the surrounding quotes.
        value = self.__source[self.__start + 1:self.__current - 1]
        self.__addToken(TokenType.STRING, value)

    def __match(self, char: str):
        if self.__isAtEnd() or self.__source[self.__current] != char:
            return False
        self.__current += 1
        return True

    def __peek(self):
        return "" if self.__isAtEnd() else self.__source[self.__current]

    def __peekNext(self):
        return "" if self.__current + 1 >= len(self.__source) else self.__source[self.__current + 1]

    def __isDigit(self, char: str):
        return char.isdecimal()

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

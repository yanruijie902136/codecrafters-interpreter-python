# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


TokenType = Enum("TokenType", [
    # Single-character tokens.
    "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE", "COMMA",
    "DOT", "MINUS", "PLUS", "SEMICOLON", "STAR", "SLASH",

    # One or two character tokens.
    "EQUAL", "EQUAL_EQUAL", "BANG", "BANG_EQUAL", "LESS", "LESS_EQUAL",
    "GREATER", "GREATER_EQUAL",

    # Literals.
    "STRING", "NUMBER", "IDENTIFIER",

    # Keywords.
    "AND", "CLASS", "ELSE", "FALSE", "FOR", "FUN", "IF", "NIL", "OR", "PRINT",
    "RETURN", "SUPER", "THIS", "TRUE", "VAR", "WHILE",

    "EOF",
])
TokenLiteral = Optional[Union[str, float]]


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: TokenLiteral
    line: int

    def __str__(self):
        return "{} {} {}".format(
            self.type.name,
            self.lexeme,
            "null" if self.literal is None else self.literal,
        )

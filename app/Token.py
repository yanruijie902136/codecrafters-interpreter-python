# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


TokenType = Enum("TokenType", [
    "EOF", "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE", "COMMA",
    "DOT", "MINUS", "PLUS", "SEMICOLON", "STAR", "EQUAL", "EQUAL_EQUAL", "BANG",
    "BANG_EQUAL", "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL", "SLASH",
    "STRING", "NUMBER",
])
TokenLiteral = Optional[Union[str, float]]


@dataclass
class Token:
    type: TokenType
    lexeme: str = ""
    literal: TokenLiteral = None

    def __str__(self):
        return "{} {} {}".format(
            self.type.name,
            self.lexeme,
            "null" if self.literal is None else self.literal,
        )

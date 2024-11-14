import dataclasses
import enum
import typing


TokenType = enum.Enum(
    "TokenType",
    [
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
    ],
)


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: typing.Any
    line: int

    def __str__(self):
        return "{} {} {}".format(self.token_type.name, self.lexeme, "null" if self.literal is None else self.literal)

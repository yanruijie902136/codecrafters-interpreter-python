import dataclasses
import enum


TokenType = enum.Enum(
    "TokenType",
    [
        "BANG",
        "BANG_EQUAL",
        "COMMA",
        "DOT",
        "EOF",
        "EQUAL",
        "EQUAL_EQUAL",
        "GREATER",
        "GREATER_EQUAL",
        "LEFT_BRACE",
        "LEFT_PAREN",
        "LESS",
        "LESS_EQUAL",
        "MINUS",
        "PLUS",
        "RIGHT_BRACE",
        "RIGHT_PAREN",
        "SEMICOLON",
        "SLASH",
        "STAR",
    ],
)


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str
    line: int

    def __str__(self) -> str:
        return "{} {} null".format(self.token_type.name, self.lexeme)

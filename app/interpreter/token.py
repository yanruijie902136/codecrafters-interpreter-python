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
        "STRING",
    ],
)


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: str | None
    line: int

    def __str__(self) -> str:
        return "{} {} {}".format(
            self.token_type.name,
            self.lexeme,
            "null" if self.literal is None else self.literal,
        )

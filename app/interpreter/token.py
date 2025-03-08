import dataclasses
import enum


TokenType = enum.Enum(
    "TokenType",
    [
        "COMMA",
        "DOT",
        "EOF",
        "EQUAL",
        "EQUAL_EQUAL",
        "LEFT_BRACE",
        "LEFT_PAREN",
        "MINUS",
        "PLUS",
        "RIGHT_BRACE",
        "RIGHT_PAREN",
        "SEMICOLON",
        "STAR",
    ],
)


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str

    def __str__(self) -> str:
        return "{} {} null".format(self.token_type.name, self.lexeme)

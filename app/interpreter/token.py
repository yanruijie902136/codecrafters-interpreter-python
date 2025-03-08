import dataclasses
import enum


TokenType = enum.Enum(
    "TokenType",
    [
        "AND",
        "BANG",
        "BANG_EQUAL",
        "COMMA",
        "CLASS",
        "DOT",
        "ELSE",
        "EOF",
        "EQUAL",
        "EQUAL_EQUAL",
        "FALSE",
        "FOR",
        "FUN",
        "GREATER",
        "GREATER_EQUAL",
        "IDENTIFIER",
        "IF",
        "LEFT_BRACE",
        "LEFT_PAREN",
        "LESS",
        "LESS_EQUAL",
        "MINUS",
        "NIL",
        "NUMBER",
        "OR",
        "PLUS",
        "PRINT",
        "RETURN",
        "RIGHT_BRACE",
        "RIGHT_PAREN",
        "SEMICOLON",
        "SLASH",
        "STAR",
        "STRING",
        "SUPER",
        "THIS",
        "TRUE",
        "VAR",
        "WHILE",
    ],
)

type TokenLiteral = str | float | None


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: TokenLiteral
    line: int

    def __str__(self) -> str:
        return "{} {} {}".format(
            self.token_type.name,
            self.lexeme,
            "null" if self.literal is None else self.literal,
        )

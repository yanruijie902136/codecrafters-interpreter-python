import dataclasses
import enum


TokenType = enum.Enum(
    "TokenType",
    [
        "EOF",
        "LEFT_PAREN",
        "RIGHT_PAREN",
    ],
)


@dataclasses.dataclass
class Token:
    token_type: TokenType
    lexeme: str

    def __str__(self) -> str:
        return "{} {} null".format(self.token_type.name, self.lexeme)

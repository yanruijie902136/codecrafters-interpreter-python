import sys

from .error import error
from .token import Token, TokenLiteral, TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self._source = source
        self._start = 0
        self._current = 0
        self._tokens = []
        self._has_error = False
        self._line = 1

        self._keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._scan_token()
            self._start = self._current
        self._add_token(TokenType.EOF)
        return self._tokens

    def has_error(self) -> bool:
        return self._has_error

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _scan_token(self) -> None:
        c = self._advance()
        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "=":
                self._add_token(TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL)
            case "!":
                self._add_token(TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG)
            case ">":
                self._add_token(TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER)
            case "<":
                self._add_token(TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS)
            case "/":
                if self._match("/"):
                    self._comment()
                else:
                    self._add_token(TokenType.SLASH)
            case "\n":
                self._line += 1
            case "\"":
                self._string()
            case _:
                if c.isspace():
                    return
                elif c.isdigit():
                    self._number()
                elif self._isalnum(c):
                    self._identifier()
                else:
                    self._error(f"Unexpected character: {c}")

    def _advance(self) -> str:
        c = self._source[self._current]
        self._current += 1
        return c

    def _add_token(self, token_type: TokenType, literal: TokenLiteral = None) -> None:
        token = Token(token_type, self._get_lexeme(), literal, self._line)
        self._tokens.append(token)

    def _get_lexeme(self) -> str:
        return self._source[self._start:self._current]

    def _error(self, message: str) -> None:
        error(self._line, message)
        self._has_error = True

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self._peek() != expected:
            return False
        self._advance()
        return True

    def _comment(self) -> None:
        while not self._is_at_end() and self._peek() != "\n":
            self._advance()

    def _peek(self) -> str:
        return "" if self._is_at_end() else self._source[self._current]

    def _string(self) -> None:
        while not self._is_at_end() and self._peek() != "\"":
            if self._advance() == "\n":
                self._line += 1

        if self._is_at_end():
            self._error("Unterminated string.")
            return
        self._advance()

        self._add_token(TokenType.STRING, self._get_lexeme()[1:-1])

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()

        self._add_token(TokenType.NUMBER, float(self._get_lexeme()))

    def _peek_next(self) -> str:
        return "" if self._current + 1 >= len(self._source) else self._source[self._current + 1]

    def _identifier(self) -> None:
        while self._isalnum(self._peek()):
            self._advance()

        token_type = self._keywords.get(self._get_lexeme(), TokenType.IDENTIFIER)
        self._add_token(token_type)

    def _isalnum(self, c: str) -> bool:
        return c == "_" or c.isalnum()

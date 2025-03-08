import sys

from .token import Token, TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self._source = source
        self._start = 0
        self._current = 0
        self._tokens = []
        self._has_error = False
        self._line = 1

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
                self._error(f"Unexpected character: {c}")

    def _advance(self) -> str:
        c = self._source[self._current]
        self._current += 1
        return c

    def _add_token(self, token_type: TokenType, literal: str | None = None) -> None:
        token = Token(token_type, self._get_lexeme(), literal, self._line)
        self._tokens.append(token)

    def _get_lexeme(self) -> str:
        return self._source[self._start:self._current]

    def _error(self, error_message: str) -> None:
        print(f"[line {self._line}] Error: {error_message}", file=sys.stderr)
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

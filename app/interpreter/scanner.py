from .token import Token, TokenType


class Scanner:
    def __init__(self, source: str) -> None:
        self._source = source
        self._start = 0
        self._current = 0
        self._tokens = []

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._scan_token()
            self._start = self._current
        self._add_token(TokenType.EOF)
        return self._tokens

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

    def _advance(self) -> str:
        c = self._source[self._current]
        self._current += 1
        return c

    def _add_token(self, token_type: TokenType) -> None:
        token = Token(token_type, self._get_lexeme())
        self._tokens.append(token)

    def _get_lexeme(self) -> str:
        return self._source[self._start:self._current]

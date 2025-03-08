from .expr import *
from .token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Expr:
        return self._expression()

    def _expression(self) -> Expr:
        return self._factor()

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            expr = BinaryExpr(left=expr, operator=self._previous(), right=self._unary())
        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            return UnaryExpr(operator=self._previous(), right=self._unary())
        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return LiteralExpr(False)
        if self._match(TokenType.TRUE):
            return LiteralExpr(True)
        if self._match(TokenType.NIL):
            return LiteralExpr(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._advance()
            return GroupingExpr(expr)

    def _match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        return False if self._is_at_end() else self._peek().token_type == token_type

    def _is_at_end(self) -> bool:
        return self._peek().token_type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

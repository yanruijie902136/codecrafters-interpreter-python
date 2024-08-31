# -*- coding: utf-8 -*-

from app.Expr import (
    AssignExpr,
    BinaryExpr,
    GroupingExpr,
    LiteralExpr,
    UnaryExpr,
    VariableExpr,
)
from app.Stmt import Stmt, ExpressionStmt, PrintStmt, VarStmt
from app.Token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.__tokens = tokens
        self.__current = 0

    def parse(self):
        return self.__expression()

    def parseStmt(self):
        statements: list[Stmt] = []
        while not self.__isAtEnd():
            statements.append(self.__declaration())
        return statements

    def __declaration(self):
        if self.__match(TokenType.VAR):
            return self.__varDeclaration()
        return self.__statement()

    def __varDeclaration(self):
        name = self.__consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = self.__expression() if self.__match(TokenType.EQUAL) else None
        self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return VarStmt(name, initializer)

    def __statement(self):
        if self.__match(TokenType.PRINT):
            return self.__printStatement()
        return self.__expressionStatement()

    def __expressionStatement(self):
        expression = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expression)

    def __printStatement(self):
        expression = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return PrintStmt(expression)

    def __expression(self):
        return self.__assignment()

    def __assignment(self):
        expr = self.__equality()
        if self.__match(TokenType.EQUAL):
            _ = self.__previous()
            value = self.__assignment()
            if isinstance(expr, VariableExpr):
                return AssignExpr(expr.name, value)
            raise RuntimeError("Invalid assignment target.")
        return expr

    def __equality(self):
        expr = self.__comparison()
        while self.__match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            expr = BinaryExpr(expr, self.__previous(), self.__comparison())
        return expr

    def __comparison(self):
        expr = self.__term()
        while self.__match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            expr = BinaryExpr(expr, self.__previous(), self.__term())
        return expr

    def __term(self):
        expr = self.__factor()
        while self.__match(TokenType.MINUS, TokenType.PLUS):
            expr = BinaryExpr(expr, self.__previous(), self.__factor())
        return expr

    def __factor(self):
        expr = self.__unary()
        while self.__match(TokenType.SLASH, TokenType.STAR):
            expr = BinaryExpr(expr, self.__previous(), self.__unary())
        return expr

    def __unary(self):
        if self.__match(TokenType.MINUS, TokenType.BANG):
            return UnaryExpr(self.__previous(), self.__unary())
        return self.__primary()

    def __primary(self):
        if self.__match(TokenType.NIL):
            return LiteralExpr(None)
        if self.__match(TokenType.FALSE):
            return LiteralExpr(False)
        if self.__match(TokenType.TRUE):
            return LiteralExpr(True)

        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.__previous().literal)

        if self.__match(TokenType.IDENTIFIER):
            return VariableExpr(self.__previous())

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise RuntimeError("Expect expression.")

    def __match(self, *types: TokenType):
        if not any(self.__check(type) for type in types):
            return False
        self.__current += 1
        return True

    def __consume(self, type: TokenType, message: str):
        if self.__check(type):
            return self.__advance()
        raise RuntimeError(message)

    def __check(self, type: TokenType):
        return False if self.__isAtEnd() else self.__peek().type is type

    def __advance(self):
        if not self.__isAtEnd():
            self.__current += 1
        return self.__previous()

    def __isAtEnd(self):
        return self.__peek().type is TokenType.EOF

    def __peek(self):
        return self.__tokens[self.__current]

    def __previous(self):
        return self.__tokens[self.__current - 1]

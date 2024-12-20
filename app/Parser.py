from app.Expr import (
    AssignExpr,
    BinaryExpr,
    CallExpr,
    Expr,
    GroupingExpr,
    LiteralExpr,
    LogicalExpr,
    UnaryExpr,
    VariableExpr,
)
from app.Stmt import (
    BlockStmt,
    ExpressionStmt,
    FunctionStmt,
    IfStmt,
    PrintStmt,
    ReturnStmt,
    Stmt,
    VarStmt,
    WhileStmt,
)
from app.Token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.__tokens = tokens
        self.__current = 0

    def parseExpr(self):
        return self.__expression()

    def parseStmt(self):
        statements: list[Stmt] = []
        while not self.__isAtEnd():
            statements.append(self.__declaration())
        return statements

    def __declaration(self):
        if self.__match(TokenType.FUN):
            return self.__function("function")
        if self.__match(TokenType.VAR):
            return self.__varDeclaration()
        return self.__statement()

    def __function(self, kind: str):
        name = self.__consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.__consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")

        parameters = []
        if not self.__check(TokenType.RIGHT_PAREN):
            while True:
                parameters.append(self.__consume(TokenType.IDENTIFIER, "Expect parameter name."))
                if not self.__match(TokenType.COMMA):
                    break
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.__consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.__block()
        return FunctionStmt(name, parameters, body)

    def __varDeclaration(self):
        name = self.__consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = self.__expression() if self.__match(TokenType.EQUAL) else None
        self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return VarStmt(name, initializer)

    def __statement(self):
        if self.__match(TokenType.LEFT_BRACE):
            return BlockStmt(self.__block())
        if self.__match(TokenType.FOR):
            return self.__forStatement()
        if self.__match(TokenType.IF):
            return self.__ifStatement()
        if self.__match(TokenType.PRINT):
            return self.__printStatement()
        if self.__match(TokenType.RETURN):
            return self.__returnStatement()
        if self.__match(TokenType.WHILE):
            return self.__whileStatement()
        return self.__expressionStatement()

    def __block(self):
        statements: list[Stmt] = []
        while not self.__check(TokenType.RIGHT_BRACE) and not self.__isAtEnd():
            statements.append(self.__declaration())
        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def __expressionStatement(self):
        expression = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expression)

    def __forStatement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.__match(TokenType.SEMICOLON):
            initializer = None
        elif self.__match(TokenType.VAR):
            initializer = self.__varDeclaration()
        else:
            initializer = self.__expressionStatement()

        condition = LiteralExpr(True) if self.__check(TokenType.SEMICOLON) else self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None if self.__check(TokenType.RIGHT_PAREN) else self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.__statement()
        if increment is not None:
            body = BlockStmt([body, ExpressionStmt(increment)])
        body = WhileStmt(condition, body)
        if initializer is not None:
            body = BlockStmt([initializer, body])
        return body

    def __ifStatement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        thenBranch = self.__statement()
        elseBranch = self.__statement() if self.__match(TokenType.ELSE) else None
        return IfStmt(condition, thenBranch, elseBranch)

    def __printStatement(self):
        expression = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return PrintStmt(expression)

    def __returnStatement(self):
        keyword = self.__previous()
        value = self.__expression() if not self.__check(TokenType.SEMICOLON) else None
        self.__consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(keyword, value)

    def __whileStatement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
        return WhileStmt(condition, self.__statement())

    def __expression(self):
        return self.__assignment()

    def __assignment(self):
        expr = self.__or()
        if self.__match(TokenType.EQUAL):
            _ = self.__previous()
            value = self.__assignment()
            if isinstance(expr, VariableExpr):
                return AssignExpr(expr.name, value)
            raise RuntimeError("Invalid assignment target.")
        return expr

    def __or(self):
        expr = self.__and()
        while self.__match(TokenType.OR):
            expr = LogicalExpr(expr, self.__previous(), self.__and())
        return expr

    def __and(self):
        expr = self.__equality()
        while self.__match(TokenType.AND):
            expr = LogicalExpr(expr, self.__previous(), self.__equality())
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
        return self.__call()

    def __call(self):
        expr = self.__primary()
        while True:
            if self.__match(TokenType.LEFT_PAREN):
                expr = self.__finishCall(expr)
            else:
                break
        return expr

    def __finishCall(self, callee: Expr):
        arguments = []
        if not self.__check(TokenType.RIGHT_PAREN):
            while True:
                arguments.append(self.__expression())
                if not self.__match(TokenType.COMMA):
                    break
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return CallExpr(callee, arguments)

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
        return False if self.__isAtEnd() else self.__peek().token_type is type

    def __advance(self):
        if not self.__isAtEnd():
            self.__current += 1
        return self.__previous()

    def __isAtEnd(self):
        return self.__peek().token_type is TokenType.EOF

    def __peek(self):
        return self.__tokens[self.__current]

    def __previous(self):
        return self.__tokens[self.__current - 1]

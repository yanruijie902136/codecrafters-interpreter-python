from .error import error
from .expr import *
from .stmt import *
from .token import Token, TokenType


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._current = 0

    def parse_to_expr(self) -> Expr:
        return self._expression()

    def parse_to_stmts(self) -> list[Stmt]:
        statements = []
        while not self._is_at_end():
            statements.append(self._declaration())
        return statements

    def _declaration(self) -> Stmt:
        if self._match(TokenType.CLASS):
            return self._class_declaration()
        if self._match(TokenType.FUN):
            return self._function("function")
        if self._match(TokenType.VAR):
            return self._var_declaration()
        return self._statement()

    def _class_declaration(self) -> ClassStmt:
        name = self._consume(TokenType.IDENTIFIER, "Expect class name.")
        self._consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")

        methods = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            methods.append(self._function("method"))

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")

        return ClassStmt(name, methods)

    def _function(self, kind: str) -> FunctionStmt:
        name = self._consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self._consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    raise self._error(self._peek(), "Can't have more than 255 parameters.")
                parameters.append(self._consume(TokenType.IDENTIFIER, "Expect parameter name."))
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self._consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        return FunctionStmt(name, parameters, self._block())

    def _var_declaration(self) -> Stmt:
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return VarStmt(name, initializer)

    def _statement(self) -> Stmt:
        if self._match(TokenType.FOR):
            return self._for_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.RETURN):
            return self._return_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.LEFT_BRACE):
            return BlockStmt(self._block())
        return self._expression_statement()

    def _for_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(TokenType.VAR):
            initializer = self._var_declaration()
        else:
            initializer = self._expression_statement()

        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self._statement()

        if increment is not None:
            body = BlockStmt([body, ExpressionStmt(increment)])

        if condition is None:
            condition = LiteralExpr(True)
        body = WhileStmt(condition, body)

        if initializer is not None:
            body = BlockStmt([initializer, body])

        return body

    def _if_statement(self) -> IfStmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self._statement()
        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()

        return IfStmt(condition, then_branch, else_branch)

    def _print_statement(self) -> PrintStmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def _return_statement(self) -> ReturnStmt:
        keyword = self._previous()
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(keyword, value)

    def _while_statement(self) -> WhileStmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        return WhileStmt(condition, self._statement())

    def _block(self) -> list[Stmt]:
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._declaration())
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def _expression_statement(self) -> ExpressionStmt:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def _expression(self) -> Expr:
        return self._assignment()

    def _assignment(self) -> Expr:
        expr = self._or()

        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, VariableExpr):
                return AssignExpr(expr.name, value)

            raise self._error(equals, "Invalid assignment target.")

        return expr

    def _or(self) -> Expr:
        expr = self._and()
        while self._match(TokenType.OR):
            expr = LogicalExpr(left=expr, operator=self._previous(), right=self._and())
        return expr

    def _and(self) -> Expr:
        expr = self._equality()
        while self._match(TokenType.AND):
            expr = LogicalExpr(left=expr, operator=self._previous(), right=self._equality())
        return expr

    def _equality(self) -> Expr:
        expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            expr = BinaryExpr(left=expr, operator=self._previous(), right=self._comparison())
        return expr

    def _comparison(self) -> Expr:
        expr = self._term()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                          TokenType.LESS, TokenType.LESS_EQUAL):
            expr = BinaryExpr(left=expr, operator=self._previous(), right=self._term())
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            expr = BinaryExpr(left=expr, operator=self._previous(), right=self._factor())
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            expr = BinaryExpr(left=expr, operator=self._previous(), right=self._unary())
        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            return UnaryExpr(operator=self._previous(), right=self._unary())
        return self._call()

    def _call(self) -> Expr:
        expr = self._primary()

        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            else:
                break

        return expr

    def _finish_call(self, callee: Expr) -> CallExpr:
        arguments = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    raise self._error(self._peek(), "Can't have more than 255 arguments.")

                arguments.append(self._expression())
                if not self._match(TokenType.COMMA):
                    break

        paren = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        return CallExpr(callee, paren, arguments)

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return LiteralExpr(False)
        if self._match(TokenType.TRUE):
            return LiteralExpr(True)
        if self._match(TokenType.NIL):
            return LiteralExpr(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self._previous().literal)

        if self._match(TokenType.IDENTIFIER):
            return VariableExpr(self._previous())

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise self._error(self._peek(), "Expect expression.")

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

    def _consume(self, token_type: TokenType, error_message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), error_message)

    def _error(self, token: Token, message: str) -> ParseError:
        error(token, message)
        return ParseError()

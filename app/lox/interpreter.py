from typing import Any

from .environment import Environment
from .expr import *
from .stmt import *
from .token import Token, TokenType


class InterpretError(Exception):
    def __init__(self, token: Token, error_message: str) -> None:
        self._token = token
        self._error_message = error_message

    def __str__(self) -> str:
        return "{}\n[line {}]".format(self._error_message, self._token.line)


class Interpreter:
    def __init__(self) -> None:
        self._environment = Environment()

    def interpret_expr(self, expr: Expr) -> None:
        value = self._evaluate(expr)
        print(self._stringify(value))

    def interpret_stmts(self, stmts: list[Stmt]) -> None:
        for stmt in stmts:
            self._execute(stmt)

    def _execute(self, stmt: Stmt) -> None:
        if isinstance(stmt, BlockStmt):
            return self._execute_block_stmt(stmt)
        if isinstance(stmt, ExpressionStmt):
            return self._execute_expression_stmt(stmt)
        if isinstance(stmt, IfStmt):
            return self._execute_if_stmt(stmt)
        if isinstance(stmt, PrintStmt):
            return self._execute_print_stmt(stmt)
        if isinstance(stmt, VarStmt):
            return self._execute_var_stmt(stmt)

    def _execute_block_stmt(self, stmt: BlockStmt) -> None:
        self._execute_block(stmt.statements, Environment(self._environment))

    def _execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self._environment
        try:
            self._environment = environment
            for stmt in statements:
                self._execute(stmt)
        finally:
            self._environment = previous

    def _execute_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self._evaluate(stmt.expression)

    def _execute_if_stmt(self, stmt: IfStmt) -> None:
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)

    def _execute_print_stmt(self, stmt: PrintStmt) -> None:
        print(self._stringify(self._evaluate(stmt.expression)))

    def _execute_var_stmt(self, stmt: VarStmt) -> None:
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self._environment.define(stmt.name.lexeme, value)

    def _evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, AssignExpr):
            return self._evaluate_assign_expr(expr)
        if isinstance(expr, BinaryExpr):
            return self._evaluate_binary_expr(expr)
        if isinstance(expr, GroupingExpr):
            return self._evaluate_grouping_expr(expr)
        if isinstance(expr, LiteralExpr):
            return self._evaluate_literal_expr(expr)
        if isinstance(expr, UnaryExpr):
            return self._evaluate_unary_expr(expr)
        if isinstance(expr, VariableExpr):
            return self._evaluate_variable_expr(expr)

    def _evaluate_assign_expr(self, expr: AssignExpr) -> Any:
        value = self._evaluate(expr.value)
        self._environment.assign(expr.name, value)
        return value

    def _evaluate_binary_expr(self, expr: BinaryExpr) -> Any:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return left - right
            case TokenType.PLUS:
                if (isinstance(left, str) and isinstance(right, str)) or \
                        (isinstance(left, float) and isinstance(right, float)):
                    return left + right
                raise InterpretError(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return left * right

    def _evaluate_grouping_expr(self, expr: GroupingExpr) -> Any:
        return self._evaluate(expr.expression)

    def _evaluate_literal_expr(self, expr: LiteralExpr) -> Any:
        return expr.value

    def _evaluate_unary_expr(self, expr: UnaryExpr) -> Any:
        right = self._evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                self._check_number_operand(expr.operator, right)
                return -right

    def _evaluate_variable_expr(self, expr: VariableExpr) -> Any:
        return self._environment.get(expr.name)

    def _is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True

    def _stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        s = str(value)
        if isinstance(value, bool):
            return s.lower()
        if isinstance(value, float) and s.endswith(".0"):
            return s[:-2]
        return s

    def _check_number_operand(self, operator: Token, right: Any) -> None:
        if isinstance(right, float):
            return
        raise InterpretError(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise InterpretError(operator, "Operands must be numbers.")

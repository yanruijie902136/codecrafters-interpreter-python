from typing import Any

from .environment import Environment
from .error import runtime_error
from .expr import *
from .lox_callable import LoxCallable, LoxClock
from .lox_class import LoxClass, LoxInstance
from .lox_function import LoxFunction
from .return_exception import ReturnException
from .stmt import *
from .token import Token, TokenType


class Interpreter:
    def __init__(self) -> None:
        self.globals = Environment()
        self.globals.define("clock", LoxClock())
        self._environment = self.globals
        self._locals: dict[Expr, int] = {}

    def interpret_expr(self, expr: Expr) -> None:
        value = self._evaluate(expr)
        print(self._stringify(value))

    def interpret_stmts(self, stmts: list[Stmt]) -> None:
        for stmt in stmts:
            self._execute(stmt)

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous = self._environment
        try:
            self._environment = environment
            for stmt in statements:
                self._execute(stmt)
        finally:
            self._environment = previous

    def resolve(self, expr: Expr, depth: int) -> None:
        self._locals[expr] = depth

    def _execute(self, stmt: Stmt) -> None:
        if isinstance(stmt, BlockStmt):
            return self._execute_block_stmt(stmt)
        if isinstance(stmt, ClassStmt):
            return self._execute_class_stmt(stmt)
        if isinstance(stmt, ExpressionStmt):
            return self._execute_expression_stmt(stmt)
        if isinstance(stmt, FunctionStmt):
            return self._execute_function_stmt(stmt)
        if isinstance(stmt, IfStmt):
            return self._execute_if_stmt(stmt)
        if isinstance(stmt, PrintStmt):
            return self._execute_print_stmt(stmt)
        if isinstance(stmt, ReturnStmt):
            return self._execute_return_stmt(stmt)
        if isinstance(stmt, VarStmt):
            return self._execute_var_stmt(stmt)
        if isinstance(stmt, WhileStmt):
            return self._execute_while_stmt(stmt)

    def _execute_block_stmt(self, stmt: BlockStmt) -> None:
        self.execute_block(stmt.statements, Environment(self._environment))

    def _execute_class_stmt(self, stmt: ClassStmt) -> None:
        self._environment.define(stmt.name.lexeme, None)
        self._environment.assign(stmt.name, LoxClass(name=stmt.name.lexeme))

    def _execute_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self._evaluate(stmt.expression)

    def _execute_function_stmt(self, stmt: FunctionStmt) -> None:
        self._environment.define(stmt.name.lexeme, LoxFunction(stmt, self._environment))

    def _execute_if_stmt(self, stmt: IfStmt) -> None:
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)

    def _execute_print_stmt(self, stmt: PrintStmt) -> None:
        print(self._stringify(self._evaluate(stmt.expression)))

    def _execute_return_stmt(self, stmt: ReturnStmt) -> None:
        value = None
        if stmt.value is not None:
            value = self._evaluate(stmt.value)
        raise ReturnException(value)

    def _execute_var_stmt(self, stmt: VarStmt) -> None:
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self._environment.define(stmt.name.lexeme, value)

    def _execute_while_stmt(self, stmt: WhileStmt) -> None:
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    def _evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, AssignExpr):
            return self._evaluate_assign_expr(expr)
        if isinstance(expr, BinaryExpr):
            return self._evaluate_binary_expr(expr)
        if isinstance(expr, CallExpr):
            return self._evaluate_call_expr(expr)
        if isinstance(expr, GetExpr):
            return self._evaluate_get_expr(expr)
        if isinstance(expr, GroupingExpr):
            return self._evaluate_grouping_expr(expr)
        if isinstance(expr, LiteralExpr):
            return self._evaluate_literal_expr(expr)
        if isinstance(expr, LogicalExpr):
            return self._evaluate_logical_expr(expr)
        if isinstance(expr, SetExpr):
            return self._evaluate_set_expr(expr)
        if isinstance(expr, UnaryExpr):
            return self._evaluate_unary_expr(expr)
        if isinstance(expr, VariableExpr):
            return self._evaluate_variable_expr(expr)

    def _evaluate_assign_expr(self, expr: AssignExpr) -> Any:
        value = self._evaluate(expr.value)
        distance = self._locals.get(expr)
        if distance is None:
            self.globals.assign(expr.name, value)
        else:
            self._environment.assign_at(distance, expr.name, value)
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
                runtime_error(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return left * right

    def _evaluate_call_expr(self, expr: CallExpr) -> Any:
        callee = self._evaluate(expr.callee)
        arguments = [self._evaluate(argument) for argument in expr.arguments]

        if not isinstance(callee, LoxCallable):
            runtime_error(expr.paren, "Can only call functions and classes.")
        if len(arguments) != callee.arity:
            runtime_error(
                expr.paren, "Expected {} arguments but got {}.".format(callee.arity, len(arguments))
            )

        return callee.call(self, arguments)

    def _evaluate_get_expr(self, expr: GetExpr) -> Any:
        obj = self._evaluate(expr.obj)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)
        runtime_error(expr.name, "Only instances have properties.")

    def _evaluate_grouping_expr(self, expr: GroupingExpr) -> Any:
        return self._evaluate(expr.expression)

    def _evaluate_literal_expr(self, expr: LiteralExpr) -> Any:
        return expr.value

    def _evaluate_logical_expr(self, expr: LogicalExpr) -> Any:
        left = self._evaluate(expr.left)
        if expr.operator.token_type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def _evaluate_set_expr(self, expr: SetExpr) -> Any:
        obj = self._evaluate(expr.obj)
        if not isinstance(obj, LoxInstance):
            runtime_error(expr.name, "Only instances have fields.")

        value = self._evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def _evaluate_unary_expr(self, expr: UnaryExpr) -> Any:
        right = self._evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                self._check_number_operand(expr.operator, right)
                return -right

    def _evaluate_variable_expr(self, expr: VariableExpr) -> Any:
        return self._look_up_variable(expr.name, expr)

    def _look_up_variable(self, name: Token, expr: Expr) -> Any:
        distance = self._locals.get(expr)
        if distance is None:
            return self.globals.get(name)
        value = self._environment.get_at(distance, name)
        return value

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
        runtime_error(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        runtime_error(operator, "Operands must be numbers.")

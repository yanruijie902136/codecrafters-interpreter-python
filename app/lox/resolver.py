import enum

from .error import error
from .expr import *
from .interpreter import Interpreter
from .stmt import *
from .token import Token


ClassType = enum.Enum("ClassType", ["NONE", "CLASS"])
FunctionType = enum.Enum("FunctionType", ["NONE", "FUNCTION", "INITIALIZER", "METHOD"])


class ResolveError(Exception):
    pass


class Resolver:
    def __init__(self, interpreter: Interpreter) -> None:
        self._interpreter = interpreter
        self._scopes: list[dict[str, bool]] = []
        self._current_class = ClassType.NONE
        self._current_function = FunctionType.NONE

    def resolve(self, statements: list[Stmt]) -> None:
        for stmt in statements:
            self._resolve(stmt)

    def _resolve(self, node: Expr | Stmt) -> None:
        if isinstance(node, AssignExpr):
            return self._resolve_assign_expr(node)
        if isinstance(node, BinaryExpr):
            return self._resolve_binary_expr(node)
        if isinstance(node, CallExpr):
            return self._resolve_call_expr(node)
        if isinstance(node, GetExpr):
            return self._resolve_get_expr(node)
        if isinstance(node, GroupingExpr):
            return self._resolve_grouping_expr(node)
        if isinstance(node, LogicalExpr):
            return self._resolve_logical_expr(node)
        if isinstance(node, SetExpr):
            return self._resolve_set_expr(node)
        if isinstance(node, ThisExpr):
            return self._resolve_this_expr(node)
        if isinstance(node, UnaryExpr):
            return self._resolve_unary_expr(node)
        if isinstance(node, VariableExpr):
            return self._resolve_variable_expr(node)

        if isinstance(node, BlockStmt):
            return self._resolve_block_stmt(node)
        if isinstance(node, ClassStmt):
            return self._resolve_class_stmt(node)
        if isinstance(node, ExpressionStmt):
            return self._resolve_expression_stmt(node)
        if isinstance(node, FunctionStmt):
            return self._resolve_function_stmt(node)
        if isinstance(node, IfStmt):
            return self._resolve_if_stmt(node)
        if isinstance(node, PrintStmt):
            return self._resolve_print_stmt(node)
        if isinstance(node, ReturnStmt):
            return self._resolve_return_stmt(node)
        if isinstance(node, VarStmt):
            return self._resolve_var_stmt(node)
        if isinstance(node, WhileStmt):
            return self._resolve_while_stmt(node)

    def _resolve_assign_expr(self, expr: AssignExpr) -> None:
        self._resolve(expr.value)
        self._resolve_local(expr, expr.name)

    def _resolve_binary_expr(self, expr: BinaryExpr) -> None:
        self._resolve(expr.left)
        self._resolve(expr.right)

    def _resolve_call_expr(self, expr: CallExpr) -> None:
        self._resolve(expr.callee)
        for argument in expr.arguments:
            self._resolve(argument)

    def _resolve_get_expr(self, expr: GetExpr) -> None:
        self._resolve(expr.obj)

    def _resolve_grouping_expr(self, expr: GroupingExpr) -> None:
        self._resolve(expr.expression)

    def _resolve_logical_expr(self, expr: LogicalExpr) -> None:
        self._resolve(expr.left)
        self._resolve(expr.right)

    def _resolve_set_expr(self, expr: SetExpr) -> None:
        self._resolve(expr.value)
        self._resolve(expr.obj)

    def _resolve_this_expr(self, expr: ThisExpr) -> None:
        if self._current_class == ClassType.NONE:
            raise self._error(expr.keyword, "Can't use 'this' outside of a class.")
        self._resolve_local(expr, expr.keyword)

    def _resolve_unary_expr(self, expr: UnaryExpr) -> None:
        self._resolve(expr.right)

    def _resolve_variable_expr(self, expr: VariableExpr) -> None:
        if self._scopes and self._scopes[-1].get(expr.name.lexeme) == False:
            raise self._error(expr.name, "Can't read local variable in its own initializer.")
        self._resolve_local(expr, expr.name)

    def _resolve_block_stmt(self, stmt: BlockStmt) -> None:
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()

    def _resolve_class_stmt(self, stmt: ClassStmt) -> None:
        enclosing_class = self._current_class
        self._current_class = ClassType.CLASS

        self._declare(stmt.name)
        self._define(stmt.name)

        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                raise self._error(stmt.superclass.name, "A class can't inherit from itself.")
            self._resolve(stmt.superclass)

        self._begin_scope()
        self._scopes[-1]["this"] = True

        for method in stmt.methods:
            function_type = FunctionType.INITIALIZER if method.name.lexeme == "init" else FunctionType.METHOD
            self._resolve_function(method, function_type)

        self._end_scope()

        self._current_class = enclosing_class

    def _resolve_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self._resolve(stmt.expression)

    def _resolve_function_stmt(self, stmt: FunctionStmt) -> None:
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt, FunctionType.FUNCTION)

    def _resolve_if_stmt(self, stmt: IfStmt) -> None:
        self._resolve(stmt.condition)
        self._resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self._resolve(stmt.else_branch)

    def _resolve_print_stmt(self, stmt: PrintStmt) -> None:
        self._resolve(stmt.expression)

    def _resolve_return_stmt(self, stmt: ReturnStmt) -> None:
        if self._current_function == FunctionType.NONE:
            raise self._error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value is not None:
            if self._current_function == FunctionType.INITIALIZER:
                raise self._error(stmt.keyword, "Can't return a value from an initializer.")
            self._resolve(stmt.value)

    def _resolve_var_stmt(self, stmt: VarStmt) -> None:
        self._declare(stmt.name)
        if stmt.initializer is not None:
            self._resolve(stmt.initializer)
        self._define(stmt.name)

    def _resolve_while_stmt(self, stmt: WhileStmt) -> None:
        self._resolve(stmt.condition)
        self._resolve(stmt.body)

    def _resolve_local(self, expr: Expr, name: Token) -> None:
        for i, scope in enumerate(reversed(self._scopes)):
            if name.lexeme in scope:
                self._interpreter.resolve(expr, depth=i)
                return

    def _resolve_function(self, function: FunctionStmt, function_type: FunctionType) -> None:
        enclosing_function = self._current_function
        self._current_function = function_type

        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self.resolve(function.body)
        self._end_scope()

        self._current_function = enclosing_function

    def _begin_scope(self) -> None:
        self._scopes.append({})

    def _end_scope(self) -> None:
        self._scopes.pop()

    def _declare(self, name: Token) -> None:
        if not self._scopes:
            return
        scope = self._scopes[-1]
        if name.lexeme in scope:
            raise self._error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def _define(self, name: Token) -> None:
        if self._scopes:
            self._scopes[-1][name.lexeme] = True

    def _error(self, name: Token, message: str) -> ResolveError:
        error(name, message)
        return ResolveError()

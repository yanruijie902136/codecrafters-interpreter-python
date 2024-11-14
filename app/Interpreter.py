from app.Environment import Environment
from app.Expr import (
    AssignExpr,
    BinaryExpr,
    CallExpr,
    Expr,
    ExprVisitor,
    GroupingExpr,
    LiteralExpr,
    LogicalExpr,
    UnaryExpr,
    VariableExpr,
)
from app.Stmt import (
    BlockStmt,
    ExpressionStmt,
    IfStmt,
    PrintStmt,
    Stmt,
    StmtVisitor,
    VarStmt,
    WhileStmt,
)
from app.Token import TokenType


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.__globals = Environment()
        self.__environment = self.__globals

        from app.LoxCallable import NativeClockFunction
        self.__globals.define("clock", NativeClockFunction())

    def interpretExpr(self, expr: Expr):
        return self.__stringify(self.__evaluate(expr))

    def interpretStmt(self, statements: list[Stmt]):
        for stmt in statements:
            self.__execute(stmt)

    ###############
    # ExprVisitor #
    ###############

    def visitAssignExpr(self, expr: AssignExpr):
        value = self.__evaluate(expr.value)
        self.__environment.assign(expr.name, value)
        return value

    def visitBinaryExpr(self, expr: BinaryExpr):
        left, right = self.__evaluate(expr.left), self.__evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.STAR:
                self.__checkNumberOperands(left, right)
                return left * right
            case TokenType.SLASH:
                self.__checkNumberOperands(left, right)
                return left / right
            case TokenType.MINUS:
                self.__checkNumberOperands(left, right)
                return left - right
            case TokenType.PLUS:
                try:
                    return left + right
                except TypeError:
                    raise RuntimeError("Operands must be two numbers or two strings.")
            case TokenType.LESS:
                self.__checkNumberOperands(left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.__checkNumberOperands(left, right)
                return left <= right
            case TokenType.GREATER:
                self.__checkNumberOperands(left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.__checkNumberOperands(left, right)
                return left >= right
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right

    def visitCallExpr(self, expr: CallExpr):
        callee = self.__evaluate(expr.callee)
        arguments = [self.__evaluate(argument) for argument in expr.arguments]
        return callee.call(self, arguments)

    def visitGroupingExpr(self, expr: GroupingExpr):
        return self.__evaluate(expr.expression)

    def visitLiteralExpr(self, expr: LiteralExpr):
        return expr.value

    def visitLogicalExpr(self, expr: LogicalExpr):
        left = self.__evaluate(expr.left)
        if expr.operator.token_type is TokenType.OR:
            if self.__isTruthy(left):
                return left
        else:
            if not self.__isTruthy(left):
                return left
        return self.__evaluate(expr.right)

    def visitUnaryExpr(self, expr: UnaryExpr):
        right = self.__evaluate(expr.right)
        match expr.operator.token_type:
            case TokenType.MINUS:
                self.__checkNumberOperand(right)
                return -right
            case TokenType.BANG:
                return not self.__isTruthy(right)

    def visitVariableExpr(self, expr: VariableExpr):
        return self.__environment.get(expr.name)

    ###############
    # StmtVisitor #
    ###############

    def visitBlockStmt(self, stmt: BlockStmt):
        previous = self.__environment
        try:
            self.__environment = Environment(self.__environment)
            for subStmt in stmt.statements:
                self.__execute(subStmt)
        finally:
            self.__environment = previous

    def visitExpressionStmt(self, stmt: ExpressionStmt):
        self.__evaluate(stmt.expression)

    def visitIfStmt(self, stmt: IfStmt):
        if self.__isTruthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.__execute(stmt.elseBranch)

    def visitPrintStmt(self, stmt: PrintStmt):
        print(self.__stringify(self.__evaluate(stmt.expression)))

    def visitVarStmt(self, stmt: VarStmt):
        value = None if stmt.initializer is None else self.__evaluate(stmt.initializer)
        self.__environment.define(stmt.name.lexeme, value)

    def visitWhileStmt(self, stmt: WhileStmt):
        while self.__isTruthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.body)

    ###################
    # Private methods #
    ###################

    def __evaluate(self, expr: Expr):
        return expr.accept(self)

    def __stringify(self, obj):
        if obj is None:
            return "nil"
        elif type(obj) is bool:
            # In Python Booleans are capitalized. In Lox they aren't.
            return str(obj).lower()
        string = str(obj)
        if type(obj) is float and string.endswith(".0"):
            string = string[:-2]
        return string

    def __isTruthy(self, obj):
        return obj is not None and obj is not False

    def __checkNumberOperand(self, operand):
        if type(operand) is not float:
            raise RuntimeError("Operand must be a number.")

    def __checkNumberOperands(self, left, right):
        if type(left) is not float or type(right) is not float:
            raise RuntimeError("Operands must be numbers.")

    def __execute(self, stmt: Stmt):
        stmt.accept(self)

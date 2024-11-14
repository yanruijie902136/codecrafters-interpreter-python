from __future__ import annotations
import abc

from app.Expr import Expr
from app.Token import Token


class Stmt(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: StmtVisitor):
        raise NotImplementedError


class StmtVisitor(abc.ABC):
    @abc.abstractmethod
    def visitBlockStmt(self, stmt: BlockStmt):
        raise NotImplementedError

    @abc.abstractmethod
    def visitExpressionStmt(self, stmt: ExpressionStmt):
        raise NotImplementedError

    @abc.abstractmethod
    def visitFunctionStmt(self, stmt: FunctionStmt):
        raise NotImplementedError

    @abc.abstractmethod
    def visitIfStmt(self, stmt: IfStmt):
        raise NotImplementedError

    @abc.abstractmethod
    def visitPrintStmt(self, stmt: PrintStmt):
        raise NotImplementedError

    @abc.abstractmethod
    def visitReturnStmt(self, stmt: ReturnStmt):
        raise NotImplementedError

    @abc.abstractmethod
    def visitVarStmt(self, stmt: VarStmt):
        raise NotImplementedError

    @abc.abstractmethod
    def visitWhileStmt(self, stmt: WhileStmt):
        raise NotImplementedError


class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor):
        return visitor.visitBlockStmt(self)


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitExpressionStmt(self)


class FunctionStmt(Stmt):
    def __init__(self, name: Token, parameters: list[Token], body: list[Stmt]):
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visitFunctionStmt(self)


class IfStmt(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt | None):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor: StmtVisitor):
        return visitor.visitIfStmt(self)


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitPrintStmt(self)


class ReturnStmt(Stmt):
    def __init__(self, keyword: Token, value: Expr | None):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor: StmtVisitor):
        return visitor.visitReturnStmt(self)


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr | None):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor):
        return visitor.visitVarStmt(self)


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visitWhileStmt(self)

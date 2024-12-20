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


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr):
        print(expr.accept(self))

    def visitAssignExpr(self, expr: AssignExpr):
        return f"(= {expr.name.lexeme} {expr.value.accept(self)})"

    def visitBinaryExpr(self, expr: BinaryExpr):
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visitCallExpr(self, expr: CallExpr):
        return f"(call {expr.callee.accept(self)} {[argument.accept(self) for argument in expr.arguments]})"

    def visitGroupingExpr(self, expr: GroupingExpr):
        return f"(group {expr.expression.accept(self)})"

    def visitLiteralExpr(self, expr: LiteralExpr):
        if expr.value is None:
            return "nil"
        if type(expr.value) is bool:
            # In Python Booleans are capitalized. In Lox they aren't.
            return str(expr.value).lower()
        return str(expr.value)

    def visitLogicalExpr(self, expr: LogicalExpr):
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visitUnaryExpr(self, expr: UnaryExpr):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"

    def visitVariableExpr(self, expr: VariableExpr):
        return expr.name.lexeme

import dataclasses


class Expr:
    pass


@dataclasses.dataclass(frozen=True)
class LiteralExpr(Expr):
    value: bool | float | None

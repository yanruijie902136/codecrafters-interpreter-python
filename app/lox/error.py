import sys

from .token import Token, TokenType


def error(location: int | Token, message: str) -> None:
    def report(line: int, where: str):
        print("[line {}] Error{}: {}".format(line, where, message), file=sys.stderr)

    if isinstance(location, int):
        report(location, "")
    else:
        where = " at end" if location.token_type == TokenType.EOF else f" at '{location.lexeme}'"
        report(location.line, where)


def runtime_error(token: Token, message: str) -> None:
    print("{}\n[line {}]".format(message, token.line), file=sys.stderr)
    raise RuntimeError

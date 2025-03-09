import argparse
import sys

import lox


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=["evaluate", "parse", "run", "tokenize"])
    parser.add_argument("filename", type=str)
    return parser.parse_args()


def tokenize(source: str, print_tokens: bool = False) -> list[lox.Token]:
    scanner = lox.Scanner(source)
    tokens = scanner.scan_tokens()
    if print_tokens:
        for token in tokens:
            print(token)
    if scanner.has_error():
        sys.exit(65)
    return tokens


def parse_to_expr(tokens: list[lox.Token], print_expr: bool = False) -> lox.Expr:
    try:
        expr = lox.Parser(tokens).parse_to_expr()
    except lox.ParseError:
        sys.exit(65)
    if print_expr:
        lox.AstPrinter().print(expr)
    return expr


def parse_to_stmts(tokens: list[lox.Token]) -> list[lox.Stmt]:
    try:
        return lox.Parser(tokens).parse_to_stmts()
    except lox.ParseError:
        sys.exit(65)


def evaluate(expr: lox.Expr) -> None:
    try:
        lox.Interpreter().interpret_expr(expr)
    except RuntimeError:
        sys.exit(70)


def run(stmts: list[lox.Stmt]) -> None:
    try:
        interpreter = lox.Interpreter()
        lox.Resolver(interpreter).resolve(stmts)
        interpreter.interpret_stmts(stmts)
    except lox.ResolveError:
        sys.exit(65)
    except RuntimeError:
        sys.exit(70)


def main() -> None:
    args = parse_args()

    with open(args.filename, mode="r") as file:
        source = file.read()

    if args.command == "tokenize":
        tokenize(source, print_tokens=True)
    elif args.command == "parse":
        parse_to_expr(tokenize(source), print_expr=True)
    elif args.command == "evaluate":
        evaluate(parse_to_expr(tokenize(source)))
    elif args.command == "run":
        run(parse_to_stmts(tokenize(source)))
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

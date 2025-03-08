import argparse
import sys

import lox


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=["evaluate", "parse", "tokenize"])
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


def parse(tokens: list[lox.Token], print_expr: bool = False) -> lox.Expr:
    try:
        expr = lox.Parser(tokens).parse()
    except lox.ParseError:
        sys.exit(65)
    if print_expr:
        lox.AstPrinter().print(expr)
    return expr


def evaluate(expr: lox.Expr) -> None:
    try:
        lox.Interpreter().interpret(expr)
    except lox.InterpretError as error:
        print(error, file=sys.stderr)
        sys.exit(70)


def main() -> None:
    args = parse_args()

    with open(args.filename, mode="r") as file:
        source = file.read()

    if args.command == "tokenize":
        tokenize(source, print_tokens=True)
    elif args.command == "parse":
        parse(tokenize(source), print_expr=True)
    elif args.command == "evaluate":
        evaluate(parse(tokenize(source)))
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

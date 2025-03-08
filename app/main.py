import argparse
import sys

from interpreter import AstPrinter, Parser, Scanner, Token


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=["parse", "tokenize"])
    parser.add_argument("filename", type=str)
    return parser.parse_args()


def tokenize(source: str, print_tokens: bool = False) -> list[Token]:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    if print_tokens:
        for token in tokens:
            print(token)
    if scanner.has_error():
        sys.exit(65)
    return tokens


def parse(tokens: list[Token]) -> None:
    parser = Parser(tokens)
    ast_printer = AstPrinter()
    print(ast_printer.print(parser.parse()))


def main() -> None:
    args = parse_args()

    with open(args.filename, mode="r") as file:
        source = file.read()

    if args.command == "tokenize":
        tokenize(source, print_tokens=True)
    elif args.command == "parse":
        parse(tokenize(source))
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

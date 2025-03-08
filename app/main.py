import argparse
import sys

from interpreter import Scanner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=["tokenize"])
    parser.add_argument("filename", type=str)
    return parser.parse_args()


def tokenize(source: str) -> None:
    scanner = Scanner(source)
    for token in scanner.scan_tokens():
        print(token)
    if scanner.has_error():
        sys.exit(65)


def main() -> None:
    args = parse_args()

    with open(args.filename, mode="r") as file:
        source = file.read()

    if args.command == "tokenize":
        tokenize(source)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

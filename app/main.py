#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from app.Scanner import Scanner


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    if command not in ["tokenize"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

    fileName = sys.argv[2]
    with open(fileName) as file:
        fileContents = file.read()

    tokens, errors = Scanner(fileContents).scanTokens()
    for token in tokens:
        print(token)
    if errors:
        for line, message in errors:
            print(f"[line {line}] Error: {message}", file=sys.stderr)
        sys.exit(65)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from app.AstPrinter import AstPrinter
from app.Expr import Expr
from app.Interpreter import Interpreter
from app.Parser import Parser
from app.Scanner import Scanner
from app.Stmt import Stmt
from app.Token import Token


def tokenize(fileContents: str, printTokens: bool = False):
    tokens, errors = Scanner(fileContents).scanTokens()
    if printTokens:
        for token in tokens:
            print(token)
    if errors:
        for line, message in errors:
            print(f"[line {line}] Error: {message}", file=sys.stderr)
        sys.exit(65)
    return tokens


def parse(tokens: list[Token], isStmt: bool = False):
    try:
        parser = Parser(tokens)
        return parser.parseStmt() if isStmt else parser.parse()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(65)


def evaluate(expr: Expr):
    try:
        return Interpreter().interpret(expr)
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(70)


def run(statements: list[Stmt]):
    Interpreter().interpretStmt(statements)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        sys.exit(1)

    fileName = sys.argv[2]
    with open(fileName) as file:
        fileContents = file.read()

    match command := sys.argv[1]:
        case "tokenize":
            tokenize(fileContents, printTokens=True)
        case "parse":
            AstPrinter().print(parse(tokenize(fileContents)))
        case "evaluate":
            print(evaluate(parse(tokenize(fileContents))))
        case "run":
            run(parse(tokenize(fileContents), isStmt=True))
        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

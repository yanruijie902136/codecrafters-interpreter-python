#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Union

from app.AstPrinter import AstPrinter
from app.Expr import Expr
from app.Interpreter import Interpreter
from app.Parser import Parser
from app.Scanner import Scanner
from app.Stmt import Stmt
from app.Token import Token


def scan(fileContents: str, printTokens: bool = False):
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


def interpret(exprOrStmts: Union[Expr, list[Stmt]]):
    try:
        interpreter = Interpreter()
        if isinstance(exprOrStmts, Expr):
            return interpreter.interpret(exprOrStmts)
        return interpreter.interpretStmt(exprOrStmts)
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(70)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        sys.exit(1)

    fileName = sys.argv[2]
    with open(fileName) as file:
        fileContents = file.read()

    match command := sys.argv[1]:
        case "tokenize":
            scan(fileContents, printTokens=True)
        case "parse":
            AstPrinter().print(parse(scan(fileContents)))
        case "evaluate":
            print(interpret(parse(scan(fileContents))))
        case "run":
            interpret(parse(scan(fileContents), isStmt=True))
        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

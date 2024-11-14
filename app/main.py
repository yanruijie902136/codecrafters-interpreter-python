import argparse
import sys

from app.AstPrinter import AstPrinter
from app.Expr import Expr
from app.Interpreter import Interpreter
from app.Parser import Parser
from app.Scanner import Scanner
from app.Stmt import Stmt
from app.Token import Token


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["tokenize", "parse", "evaluate", "run"])
    parser.add_argument("fileName", type=str)
    return parser.parse_args()


def scan(fileContents: str, printTokens=False):
    tokens, errors = Scanner(fileContents).scanTokens()
    if printTokens:
        for token in tokens:
            print(token)
    if errors:
        for line, message in errors:
            print(f"[line {line}] Error: {message}", file=sys.stderr)
        sys.exit(65)
    return tokens


def parse(tokens: list[Token], isStmt=False):
    try:
        parser = Parser(tokens)
        return parser.parseStmt() if isStmt else parser.parseExpr()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(65)


def interpret(exprOrStmts: Expr | list[Stmt]):
    try:
        interpreter = Interpreter()
        if isinstance(exprOrStmts, Expr):
            return interpreter.interpretExpr(exprOrStmts)
        return interpreter.interpretStmt(exprOrStmts)
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(70)


def main():
    args = parseArgs()

    with open(args.fileName) as file:
        fileContents = file.read()

    match args.command:
        case "tokenize":
            scan(fileContents, printTokens=True)
        case "parse":
            AstPrinter().print(parse(scan(fileContents)))
        case "evaluate":
            print(interpret(parse(scan(fileContents))))
        case "run":
            interpret(parse(scan(fileContents), isStmt=True))


if __name__ == "__main__":
    main()

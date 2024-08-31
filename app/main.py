import sys


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

    if fileContents:
        raise NotImplementedError("Scanner not implemented")
    else:
        print("EOF  null")


if __name__ == "__main__":
    main()

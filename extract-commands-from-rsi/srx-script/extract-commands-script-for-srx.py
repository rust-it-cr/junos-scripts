import pathlib
import re
import sys


DATA = []

with open("srx-commands.csv") as file:
    for line in file:
        DATA.append(line.strip())


def main():
    try:
        text, type = read_rsi()

        show_commands = []

        if type == "standalone":
            for item in DATA:
                show_commands.append(extract_commands(text, item))
        elif type == "cluster":
            number = 0
            for node in text:
                show_commands.append([f"===> BEGINNING - NODE{number} <===\n"])
                for item in DATA:
                    show_commands.append(extract_commands(node, item))
                show_commands.append([f"===> ENDING - NODE{number} <===\n"])
                number += 1

        result = create_file(show_commands)
        sys.exit(result)

    except Exception as e:
        sys.exit(f"Failure: {e}. Please try again or report this to the creator of this script.")


def read_rsi():
    with open(sys.argv[1], "r") as file:
        lines = file.readlines()

    if "node" in lines[0]:
        half = int(len(lines) / 2)

        lines1 = lines[:half]
        lines2 = lines[half:]

        for line in lines2:
            if "show version detail no-forwarding" in line:
                return [lines1, lines2], "cluster"
            else:
                continue

    return lines, "standalone"


def extract_commands(lines, command):
    switch = False
    next_command = "^.+@?.+> .+$"
    tmp = []

    for line in lines:
        if command in line:
            switch = True
            tmp.append(line.strip())
        elif switch and not re.match(next_command, line):
            tmp.append(line.strip())
        elif re.match(next_command, line):
            switch = False

    return tmp


def create_file(show_commands):
    path = pathlib.Path.home() / "Downloads" / f"{sys.argv[2]}.txt"

    with open(f"{path}", "w") as file:

        for element in show_commands:

            for line in element:
                file.write(f"{line}\n")

    return f"{path} has been successfully generated!"


if __name__ == "__main__":
    main()
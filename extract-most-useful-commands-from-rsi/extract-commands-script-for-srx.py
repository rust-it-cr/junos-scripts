import csv
import pathlib
import sys


DATA = []

with open("srx-commands.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        DATA.append(row)


def main():
    try:
        text, type = read_rsi()

        show_commands = []

        if type == "standalone":
            show_commands.append([f"===> STANDALONE <===\n"])
            for item in DATA:
                show_commands.append(extract_commands(text, item))
        elif type == "cluster":
            number = 0
            for node in text:
                show_commands.append([f"===> NODE {number} <===\n"])
                number += 1
                for item in DATA:
                    show_commands.append(extract_commands(node, item))

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
    
        second_rsi_half_health = False

        for line in lines2:
            if "show version detail no-forwarding" in line:
                second_rsi_half_health = True
                break
            else:
                continue

        if second_rsi_half_health:
            return [lines1, lines2], "cluster"
    
    else:
        return lines, "standalone"


def extract_commands(lines, commands):
    switch = False
    tmp = []

    for line in lines:
        if commands["first"] in line:
            switch = True
        if switch and commands["last"] not in line:
            tmp.append(line.strip())
        if commands["last"] in line:
            break

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
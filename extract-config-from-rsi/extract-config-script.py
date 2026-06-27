import pathlib
import re
import sys


def main():
    try:
        file = sys.argv[1]
        rsi_lines = read_rsi(file)
        config = purge_config(rsi_lines)
        result = create_file(config)
        sys.exit(result)
    except Exception as e:
        sys.exit(f"Failure: {e}. Please try again.")


def read_rsi(file):
    with open(file, "r") as open_file:
        lines = open_file.readlines()

    return lines


def purge_config(configuration):
    switch = False
    config_number = 0
    config_start = "show configuration | except SECRET-DATA"
    next_command = "^.+@.+> .+$"
    tmp = []

    for line in configuration:
        if config_start in line:
            switch = True
            config_number += 1
        elif "Last commit" in line:
            pass
        elif "tnpdump" in line:
            switch = False
        elif switch and not re.match(next_command, line):
            tmp.append(line.strip())
        elif re.match(next_command, line):
            switch = False
        elif config_number == 1:
            break

    return tmp


def create_file(configuration):
    path = pathlib.Path.home() / "Downloads" / f"{sys.argv[2]}.txt"

    with open(f"{path}", "w") as file:
        for line in configuration:
            file.write(f"{line}\n")

    return f"{path} has been successfully created!"


if __name__ == "__main__":
    main()
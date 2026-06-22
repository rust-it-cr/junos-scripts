import pathlib
import re
import sys


DATA = [
    'show system uptime no-forwarding',
    'show version detail no-forwarding',
    'show chassis hardware detail no-forwarding',
    'show system license',
    'show system core-dumps no-forwarding',
    'show system storage no-forwarding',
    'show system snapshot media internal',
    'show chassis alarms no-forwarding',
    'show chassis routing-engine no-forwarding',
    'show system processes extensive no-forwarding',
    'show chassis environment no-forwarding',
    'show security monitoring fpc 0',
    'show chassis firmware no-forwarding',
    'show system firmware no-forwarding',
    'show arp no-resolve',
    'show route summary',
    'show route brief',
    'show system commit',
    'show system configuration database usage',
    'show chassis cluster status',
    'show chassis cluster statistics',
    'show chassis cluster interfaces',
    'show chassis cluster information detail no-forwarding',
    'show security flow statistics',
    'show security flow status',
    'show security flow session summary no-forwarding',
    'request pfe execute command "show version" target',
    'request pfe execute command "show arena" target',
    'request pfe execute command "show memory" target'
]


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
                show_commands.append([f"=== BEGINNING - NODE{number} ===\n"])
                for item in DATA:
                    show_commands.append(extract_commands(node, item))
                show_commands.append([f"=== ENDING - NODE{number} ===\n"])
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


def extract_commands(lines, command):
    switch = False
    next_command = "^.+@.+> .+$"
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
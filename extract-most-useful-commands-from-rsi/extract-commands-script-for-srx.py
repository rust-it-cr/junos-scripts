import pathlib
import sys


DATA = [
    {'first': 'show system uptime', 'last': 'show pfe statistics error'},
    {'first': 'show chassis routing-engine', 'last': 'show chassis fpc detail'},
    {'first': 'show system storage', 'last': 'show system virtual-memory'},
    {'first': 'show route summary', 'last': 'file list detail'},
    {'first': 'show chassis cluster status', 'last': 'request pfe execute command "show usp ha vsd"'},
    {'first': 'request pfe execute command "show version"', 'last': 'request pfe execute command "show threads"'},
    {'first': 'request pfe execute command "show pfe statistics traffic"', 'last': 'request pfe execute command "show fwdd statistics result"'},
    {'first': 'request pfe execute command "show arena"', 'last': 'request pfe execute command "show services mum"'},
    {'first': 'show security monitoring fpc', 'last': 'show services advanced-anti-malware'},
    {'first': 'show security flow statistics', 'last': 'request pfe execute command "show usp interface all"'}
]


def main():
    text, type = read_rsi()

    show_commands = []

    if type == "standalone":
        show_commands.append([f"===> STANDALONE <===\n"])
        for item in DATA:
            show_commands.append(extract_commands(text, item))
    elif type == "cluster":
        number = 0
        for node in text:
            show_commands.append([f"===> NODE{number} <===\n"])
            number += 1
            for item in DATA:
                show_commands.append(extract_commands(node, item))

    result = create_file(show_commands)
    sys.exit(result)


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
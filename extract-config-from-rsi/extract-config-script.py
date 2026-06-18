import pathlib
import sys


def main(): # USAGE ==> python3 <source-path-for-script> <source-path-for-rsi-file> <resulting-file-name> | it will save the resulting file to the Downloads folder
    try:
        file = sys.argv[1]
        config = read_rsi(file)
        config = purge_config(config)
        result = create_file(config)
    except Exception as e:
        sys.exit(f"Failure: {e}. Please try again.")

def read_rsi(file):
    with open(file, "r") as open_file:
        lines = open_file.readlines()

        inside_range = False
        config_lines = []

        for line in lines:
            if "show configuration | except SECRET-DATA" in line:
                inside_range = True
            if inside_range:
                config_lines.append(line.strip())
            if "show interfaces extensive no-forwarding" in line:
                break

    return config_lines


def purge_config(configuration):
    tmp = []
    
    for element in configuration:
        if "show configuration | except SECRET-DATA" in element or "show interfaces extensive no-forwarding" in element or "Last commit" in element:
            pass
        elif not element:
            pass
        else:
            tmp.append(element)

    return tmp


def create_file(configuration):
    path = pathlib.Path.home() / "Downloads" / f"{sys.argv[2]}.txt"

    with open(f"{path}", "w") as file:
        for line in configuration:
            file.write(f"{line}\n")


if __name__ == "__main__":
    main() 
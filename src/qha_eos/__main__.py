import argparse

def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--json', type=str)
    argument_parser.add_argument('--txt', type=str)
    namespace = argument_parser.parse_args()

    if namespace.json:
        from .reader import JSONInputReader
        reader = JSONInputReader()
        data = reader.read(namespace.json)
    elif namespace.txt:
        from .reader import TabularInputReader
        reader = TabularInputReader()
        data = reader.read(namespace.txt)
    else:
        argument_parser.print_help()
        exit()